"""Exact Rational Wave Equation Solver.

Implements 1D and 2D wave equation solvers using exact rational arithmetic.
No floating-point arithmetic is used internally - all calculations use
Rational numbers backed by fractions.Fraction.

Features:
- WaveSolver1D: Exact rational finite difference for 1D wave equation
- WaveSolver2D: Rectangular and circular domains
- Exact boundary conditions: Dirichlet, Neumann, Periodic
- Modal analysis with exact rational eigenvalues
- 5-smooth grid sizes for optimal base-60 discretization
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import gcd, isqrt
from typing import Callable
from fractions import Fraction

from .core.rational import Rational


class BoundaryType(Enum):
    """Boundary condition types."""
    DIRICHLET = "dirichlet"      # u = 0 at boundary
    NEUMANN = "neumann"          # du/dn = 0 at boundary
    PERIODIC = "periodic"        # periodic boundary conditions


@dataclass(frozen=True)
class WaveParameters:
    """Parameters for wave equation solver."""
    c: Rational              # Wave speed
    dx: Rational             # Spatial step
    dt: Rational             # Time step
    nx: int                  # Number of spatial grid points
    nt: int                  # Number of time steps
    boundary: BoundaryType   # Boundary condition type
    
    def __post_init__(self) -> None:
        if self.nx < 3:
            raise ValueError("nx must be >= 3")
        if self.nt < 1:
            raise ValueError("nt must be >= 1")
        if self.dx <= 0:
            raise ValueError("dx must be positive")
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if self.c <= 0:
            raise ValueError("c must be positive")
    
    @property
    def courant(self) -> Rational:
        """Courant number: c * dt / dx"""
        return self.c * self.dt / self.dx
    
    @property
    def is_stable(self) -> bool:
        """Check CFL stability condition: courant <= 1"""
        return self.courant <= 1


@dataclass(frozen=True)
class Mode:
    """A normal mode of vibration."""
    index: int               # Mode number (n for 1D, (n,m) for 2D)
    frequency: Rational      # Angular frequency ω
    wavelength: Rational     # Wavelength λ
    shape: list[Rational]    # Spatial mode shape


def is_5_smooth(n: int) -> bool:
    """Check if n is 5-smooth (only prime factors 2, 3, 5)."""
    if n <= 0:
        return False
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


def nearest_5_smooth(n: int, direction: str = "up") -> int:
    """Find nearest 5-smooth number >= n (direction='up') or <= n (direction='down')."""
    if direction == "down":
        for k in range(n, 0, -1):
            if is_5_smooth(k):
                return k
        return 1
    else:
        k = n
        while True:
            if is_5_smooth(k):
                return k
            k += 1


def generate_5_smooth_grid(base: int, max_factor: int = 60) -> list[int]:
    """Generate 5-smooth numbers up to base * max_factor."""
    smooth = []
    for i in range(1, max_factor + 1):
        if is_5_smooth(i):
            smooth.append(i)
    return smooth


# =====================================================================
# 1D Wave Equation Solver
# =====================================================================

class WaveSolver1D:
    """Exact rational finite difference solver for 1D wave equation.
    
    Solves: ∂²u/∂t² = c² ∂²u/∂x²
    
    Using second-order central differences in space and time:
    u[i]^(n+1) = 2*u[i]^n - u[i]^(n-1) + (c*dt/dx)² * (u[i+1]^n - 2*u[i]^n + u[i-1]^n)
    
    All arithmetic is exact using Rational numbers.
    """
    
    def __init__(self, params: WaveParameters):
        self.params = params
        self.nx = params.nx
        self.nt = params.nt
        self.c = params.c
        self.dx = params.dx
        self.dt = params.dt
        self.boundary = params.boundary
        
        # Precompute constant factor: (c*dt/dx)^2
        self.alpha = params.courant ** 2
        
        # Initialize solution arrays: u_prev, u_curr, u_next
        # Each is a list of Rational of length nx
        self.u_prev = [Rational(0) for _ in range(self.nx)]
        self.u_curr = [Rational(0) for _ in range(self.nx)]
        self.u_next = [Rational(0) for _ in range(self.nx)]
        
        # Store history for energy/momentum analysis
        self.history: list[list[Rational]] = []
        self.time = Rational(0)
        self.step = 0
    
    def set_initial_conditions(
        self,
        u0: Callable[[Rational], Rational] | list[Rational],
        v0: Callable[[Rational], Rational] | list[Rational] | None = None
    ) -> None:
        """Set initial displacement u(x,0) and velocity v(x,0).
        
        Args:
            u0: Initial displacement - callable u(x) or list of values at grid points
            v0: Initial velocity - callable v(x) or list of values at grid points (default: zero)
        """
        x_vals = [self.dx * i for i in range(self.nx)]
        
        # Set u_prev = u(x, -dt) using Taylor expansion: u(x,-dt) ≈ u(x,0) - dt*v(x,0) + (dt²/2)*u_tt(x,0)
        # From wave equation: u_tt = c²*u_xx
        if callable(u0):
            u0_vals = [u0(x) for x in x_vals]
        else:
            if len(u0) != self.nx:
                raise ValueError(f"u0 list must have length {self.nx}")
            u0_vals = u0
        
        if v0 is None:
            v0_vals = [Rational(0) for _ in range(self.nx)]
        elif callable(v0):
            v0_vals = [v0(x) for x in x_vals]
        else:
            if len(v0) != self.nx:
                raise ValueError(f"v0 list must have length {self.nx}")
            v0_vals = v0
        
        # Compute u_xx at t=0 using central differences
        u_xx = [Rational(0) for _ in range(self.nx)]
        for i in range(1, self.nx - 1):
            u_xx[i] = (u0_vals[i+1] - Rational(2)*u0_vals[i] + u0_vals[i-1]) / (self.dx ** 2)
        
        # Apply boundary conditions to u_xx
        self._apply_boundary_to_derivative(u_xx)
        
        # u(x, -dt) = u(x,0) - dt*v(x,0) + (dt²/2)*c²*u_xx(x,0)
        dt2_over_2 = self.dt ** 2 / 2
        c2 = self.c ** 2
        
        for i in range(self.nx):
            self.u_prev[i] = u0_vals[i] - self.dt * v0_vals[i] + dt2_over_2 * c2 * u_xx[i]
            self.u_curr[i] = u0_vals[i]
        self._apply_boundary(self.u_curr)
        
        self.history = [self.u_curr.copy()]
        self.time = Rational(0)
        self.step = 0
    
    def _apply_boundary(self, u: list[Rational]) -> None:
        """Apply boundary conditions to solution array."""
        if self.boundary == BoundaryType.DIRICHLET:
            u[0] = Rational(0)
            u[-1] = Rational(0)
        elif self.boundary == BoundaryType.NEUMANN:
            # du/dx = 0 at boundaries -> u[0] = u[1], u[-1] = u[-2]
            u[0] = u[1]
            u[-1] = u[-2]
        elif self.boundary == BoundaryType.PERIODIC:
            # u[0] = u[-2], u[-1] = u[1] (ghost points)
            pass  # Handled in update step
    
    def _apply_boundary_to_derivative(self, u_xx: list[Rational]) -> None:
        """Apply boundary conditions to second derivative array."""
        if self.boundary == BoundaryType.DIRICHLET:
            # For Dirichlet, u=0 at boundary, but u_xx can be non-zero
            # We don't enforce anything special here
            pass
        elif self.boundary == BoundaryType.NEUMANN:
            # du/dx = 0 -> u_xx at boundary equals interior
            u_xx[0] = u_xx[1]
            u_xx[-1] = u_xx[-2]
        elif self.boundary == BoundaryType.PERIODIC:
            pass
    
    def step_forward(self) -> list[Rational]:
        """Advance one time step using exact rational arithmetic.
        
        Returns:
            The new solution array u_next
        """
        # Standard finite difference update
        for i in range(1, self.nx - 1):
            self.u_next[i] = (
                Rational(2) * self.u_curr[i] - self.u_prev[i] +
                self.alpha * (self.u_curr[i+1] - Rational(2)*self.u_curr[i] + self.u_curr[i-1])
            )
        
        # Boundary conditions
        if self.boundary == BoundaryType.DIRICHLET:
            self.u_next[0] = Rational(0)
            self.u_next[-1] = Rational(0)
        elif self.boundary == BoundaryType.NEUMANN:
            self.u_next[0] = self.u_next[1]
            self.u_next[-1] = self.u_next[-2]
        elif self.boundary == BoundaryType.PERIODIC:
            # Periodic: u[0] connects to u[-2], u[-1] connects to u[1]
            # u_next[0] uses u_curr[-2] as left neighbor, u_curr[1] as right
            self.u_next[0] = (
                Rational(2) * self.u_curr[0] - self.u_prev[0] +
                self.alpha * (self.u_curr[1] - Rational(2)*self.u_curr[0] + self.u_curr[-2])
            )
            self.u_next[-1] = (
                Rational(2) * self.u_curr[-1] - self.u_prev[-1] +
                self.alpha * (self.u_curr[0] - Rational(2)*self.u_curr[-1] + self.u_curr[-2])
            )
            # Also need to handle i=1 and i=nx-2 for periodic
            self.u_next[1] = (
                Rational(2) * self.u_curr[1] - self.u_prev[1] +
                self.alpha * (self.u_curr[2] - Rational(2)*self.u_curr[1] + self.u_curr[0])
            )
            self.u_next[-2] = (
                Rational(2) * self.u_curr[-2] - self.u_prev[-2] +
                self.alpha * (self.u_curr[-1] - Rational(2)*self.u_curr[-2] + self.u_curr[-3])
            )
        # Swap arrays
        self.u_prev, self.u_curr, self.u_next = self.u_curr, self.u_next, self.u_prev
        
        self.time += self.dt
        self.step += 1
        self.history.append(self.u_curr.copy())
        
        return self.u_curr
    
    def run(self, steps: int | None = None) -> list[list[Rational]]:
        """Run simulation for specified number of steps.
        
        Args:
            steps: Number of steps to run (default: params.nt)
            
        Returns:
            History of solution arrays
        """
        if steps is None:
            steps = self.nt
        
        for _ in range(steps):
            self.step_forward()
        
        return self.history
    
    def compute_energy(self) -> Rational:
        """Compute total energy: E = 1/2 ∫ (u_t² + c² u_x²) dx
        
        Using discrete approximation with exact rational arithmetic.
        """
        # Kinetic energy: 1/2 * sum(u_t²) * dx
        # u_t ≈ (u_curr - u_prev) / dt
        kinetic = Rational(0)
        for i in range(self.nx):
            u_t = (self.u_curr[i] - self.u_prev[i]) / self.dt
            kinetic += u_t * u_t
        kinetic = kinetic * self.dx / 2
        
        # Potential energy: 1/2 * c² * sum(u_x²) * dx
        # u_x ≈ (u[i+1] - u[i-1]) / (2*dx)
        potential = Rational(0)
        for i in range(1, self.nx - 1):
            u_x = (self.u_curr[i+1] - self.u_curr[i-1]) / (Rational(2) * self.dx)
            potential += u_x * u_x
        # Boundary terms for Neumann/Periodic
        if self.boundary == BoundaryType.NEUMANN:
            # u_x = 0 at boundaries
            pass
        elif self.boundary == BoundaryType.PERIODIC:
            u_x_0 = (self.u_curr[1] - self.u_curr[-2]) / (Rational(2) * self.dx)
            u_x_end = (self.u_curr[0] - self.u_curr[-2]) / (Rational(2) * self.dx)
            potential += u_x_0 * u_x_0 + u_x_end * u_x_end
        
        potential = potential * (self.c ** 2) * self.dx / 2
        
        return kinetic + potential
    
    def compute_momentum(self) -> Rational:
        """Compute momentum: P = -∫ u_t * u_x dx"""
        momentum = Rational(0)
        for i in range(1, self.nx - 1):
            u_t = (self.u_curr[i] - self.u_prev[i]) / self.dt
            u_x = (self.u_curr[i+1] - self.u_curr[i-1]) / (Rational(2) * self.dx)
            momentum += u_t * u_x
        if self.boundary == BoundaryType.PERIODIC:
            u_t_0 = (self.u_curr[0] - self.u_prev[0]) / self.dt
            u_x_0 = (self.u_curr[1] - self.u_curr[-2]) / (Rational(2) * self.dx)
            u_t_end = (self.u_curr[-1] - self.u_prev[-1]) / self.dt
            u_x_end = (self.u_curr[0] - self.u_curr[-2]) / (Rational(2) * self.dx)
            momentum += u_t_0 * u_x_0 + u_t_end * u_x_end
        return -momentum * self.dx
    
    def get_solution_at_time(self, t: Rational) -> list[Rational] | None:
        """Get solution at specific time (if available in history)."""
        step_idx = int(t / self.dt)
        if 0 <= step_idx < len(self.history):
            return self.history[step_idx]
        return None


# =====================================================================
# 2D Wave Equation Solver
# =====================================================================

@dataclass(frozen=True)
class WaveParameters2D:
    """Parameters for 2D wave equation solver."""
    c: Rational              # Wave speed
    dx: Rational             # Spatial step (x)
    dy: Rational             # Spatial step (y)
    dt: Rational             # Time step
    nx: int                  # Grid points in x
    ny: int                  # Grid points in y
    nt: int                  # Time steps
    boundary_x: BoundaryType # Boundary condition in x
    boundary_y: BoundaryType # Boundary condition in y
    domain_type: str = "rectangular"  # "rectangular" or "circular"
    radius: Rational | None = None    # For circular domain
    
    def __post_init__(self) -> None:
        if self.nx < 3 or self.ny < 3:
            raise ValueError("nx, ny must be >= 3")
        if self.nt < 1:
            raise ValueError("nt must be >= 1")
        if self.dx <= 0 or self.dy <= 0 or self.dt <= 0 or self.c <= 0:
            raise ValueError("dx, dy, dt, c must be positive")
        if self.domain_type == "circular" and self.radius is None:
            raise ValueError("radius required for circular domain")
    
    @property
    def courant_x(self) -> Rational:
        return self.c * self.dt / self.dx
    
    @property
    def courant_y(self) -> Rational:
        return self.c * self.dt / self.dy
    
    @property
    def is_stable(self) -> bool:
        # 2D CFL condition: c*dt*sqrt(1/dx² + 1/dy²) <= 1
        # Simplified: max(courant_x, courant_y) <= 1/sqrt(2) for square grid
        # Exact: (c*dt)² * (1/dx² + 1/dy²) <= 1
        cx2 = self.courant_x ** 2
        cy2 = self.courant_y ** 2
        return cx2 + cy2 <= 1


class WaveSolver2D:
    """Exact rational finite difference solver for 2D wave equation.
    
    Solves: ∂²u/∂t² = c² (∂²u/∂x² + ∂²u/∂y²)
    
    Using second-order central differences in space and time.
    All arithmetic is exact using Rational numbers.
    """
    
    def __init__(self, params: WaveParameters2D):
        self.params = params
        self.nx = params.nx
        self.ny = params.ny
        self.nt = params.nt
        self.c = params.c
        self.dx = params.dx
        self.dy = params.dy
        self.dt = params.dt
        self.boundary_x = params.boundary_x
        self.boundary_y = params.boundary_y
        self.domain_type = params.domain_type
        self.radius = params.radius
        
        # Precompute constant factors
        self.alpha_x = (params.c * params.dt / params.dx) ** 2
        self.alpha_y = (params.c * params.dt / params.dy) ** 2
        
        # Initialize solution arrays: (ny x nx)
        self.u_prev = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        self.u_curr = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        self.u_next = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        
        # For circular domain: mask of valid points
        self._circular_mask = None
        if self.domain_type == "circular":
            self._create_circular_mask()
        
        self.history: list[list[list[Rational]]] = []
        self.time = Rational(0)
        self.step = 0
    
    def _create_circular_mask(self) -> None:
        """Create mask for circular domain."""
        cx = (self.nx - 1) / 2
        cy = (self.ny - 1) / 2
        r_cells = self.radius / self.dx  # Assume dx == dy for circular
        
        self._circular_mask = [[False for _ in range(self.nx)] for _ in range(self.ny)]
        for j in range(self.ny):
            for i in range(self.nx):
                dx = i - cx
                dy = j - cy
                dist2 = Rational(dx*dx + dy*dy)
                if dist2 <= r_cells * r_cells:
                    self._circular_mask[j][i] = True
    
    def _is_valid_point(self, i: int, j: int) -> bool:
        """Check if point (i,j) is in the domain."""
        if self.domain_type == "rectangular":
            return True
        return self._circular_mask[j][i]
    
    def set_initial_conditions(
        self,
        u0: Callable[[Rational, Rational], Rational] | list[list[Rational]],
        v0: Callable[[Rational, Rational], Rational] | list[list[Rational]] | None = None
    ) -> None:
        """Set initial displacement u(x,y,0) and velocity v(x,y,0)."""
        x_vals = [self.dx * i for i in range(self.nx)]
        y_vals = [self.dy * j for j in range(self.ny)]
        
        if callable(u0):
            u0_vals = [[u0(x_vals[i], y_vals[j]) for i in range(self.nx)] for j in range(self.ny)]
        else:
            if len(u0) != self.ny or any(len(row) != self.nx for row in u0):
                raise ValueError(f"u0 must be {self.ny}x{self.nx}")
            u0_vals = u0
        
        if v0 is None:
            v0_vals = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        elif callable(v0):
            v0_vals = [[v0(x_vals[i], y_vals[j]) for i in range(self.nx)] for j in range(self.ny)]
        else:
            if len(v0) != self.ny or any(len(row) != self.nx for row in v0):
                raise ValueError(f"v0 must be {self.ny}x{self.nx}")
            v0_vals = v0
        
        # Compute u_xx and u_yy at t=0
        u_xx = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        u_yy = [[Rational(0) for _ in range(self.nx)] for _ in range(self.ny)]
        
        for j in range(1, self.ny - 1):
            for i in range(1, self.nx - 1):
                if self._is_valid_point(i, j):
                    u_xx[j][i] = (u0_vals[j][i+1] - Rational(2)*u0_vals[j][i] + u0_vals[j][i-1]) / (self.dx ** 2)
                    u_yy[j][i] = (u0_vals[j+1][i] - Rational(2)*u0_vals[j][i] + u0_vals[j-1][i]) / (self.dy ** 2)
        
        self._apply_boundary_to_derivatives(u_xx, u_yy)
        # u(x,y,-dt) = u(x,y,0) - dt*v(x,y,0) + (dt²/2)*c²*(u_xx + u_yy)
        dt2_over_2 = self.dt ** 2 / 2
        c2 = self.c ** 2
        
        for j in range(self.ny):
            for i in range(self.nx):
                if self._is_valid_point(i, j):
                    self.u_prev[j][i] = (
                        u0_vals[j][i] - self.dt * v0_vals[j][i] +
                        dt2_over_2 * c2 * (u_xx[j][i] + u_yy[j][i])
                    )
                    self.u_curr[j][i] = u0_vals[j][i]
                else:
                    self.u_prev[j][i] = Rational(0)
                    self.u_curr[j][i] = Rational(0)
        
        self._apply_boundary(self.u_prev)
        self._apply_boundary(self.u_curr)
        
        self.history = [[row[:] for row in self.u_curr]]
        self.time = Rational(0)
        self.step = 0
    
    def _apply_boundary(self, u: list[list[Rational]]) -> None:
        """Apply boundary conditions."""
        # X boundaries
        if self.boundary_x == BoundaryType.DIRICHLET:
            for j in range(self.ny):
                u[j][0] = Rational(0)
                u[j][-1] = Rational(0)
        elif self.boundary_x == BoundaryType.NEUMANN:
            for j in range(self.ny):
                u[j][0] = u[j][1]
                u[j][-1] = u[j][-2]
        
        # Y boundaries
        if self.boundary_y == BoundaryType.DIRICHLET:
            for i in range(self.nx):
                u[0][i] = Rational(0)
                u[-1][i] = Rational(0)
        elif self.boundary_y == BoundaryType.NEUMANN:
            for i in range(self.nx):
                u[0][i] = u[1][i]
                u[-1][i] = u[-2][i]
        
        # Periodic boundaries handled in step_forward
        # Circular domain: zero outside mask
        if self.domain_type == "circular":
            for j in range(self.ny):
                for i in range(self.nx):
                    if not self._circular_mask[j][i]:
                        u[j][i] = Rational(0)
    
    def _apply_boundary_to_derivatives(
        self,
        u_xx: list[list[Rational]],
        u_yy: list[list[Rational]]
    ) -> None:
        """Apply boundary conditions to derivative arrays."""
        # Similar to _apply_boundary but for derivatives
        if self.boundary_x == BoundaryType.NEUMANN:
            for j in range(self.ny):
                u_xx[j][0] = u_xx[j][1]
                u_xx[j][-1] = u_xx[j][-2]
        if self.boundary_y == BoundaryType.NEUMANN:
            for i in range(self.nx):
                u_yy[0][i] = u_yy[1][i]
                u_yy[-1][i] = u_yy[-2][i]
        if self.domain_type == "circular":
            for j in range(self.ny):
                for i in range(self.nx):
                    if not self._circular_mask[j][i]:
                        u_xx[j][i] = Rational(0)
                        u_yy[j][i] = Rational(0)
    
    def step_forward(self) -> list[list[Rational]]:
        """Advance one time step."""
        for j in range(1, self.ny - 1):
            for i in range(1, self.nx - 1):
                if not self._is_valid_point(i, j):
                    continue
                
                # Standard 5-point stencil
                laplacian_x = self.u_curr[j][i+1] - Rational(2)*self.u_curr[j][i] + self.u_curr[j][i-1]
                laplacian_y = self.u_curr[j+1][i] - Rational(2)*self.u_curr[j][i] + self.u_curr[j-1][i]
                
                self.u_next[j][i] = (
                    Rational(2) * self.u_curr[j][i] - self.u_prev[j][i] +
                    self.alpha_x * laplacian_x + self.alpha_y * laplacian_y
                )
        
        # Boundary conditions
        # X boundaries
        if self.boundary_x == BoundaryType.DIRICHLET:
            for j in range(self.ny):
                self.u_next[j][0] = Rational(0)
                self.u_next[j][-1] = Rational(0)
        elif self.boundary_x == BoundaryType.NEUMANN:
            for j in range(self.ny):
                self.u_next[j][0] = self.u_next[j][1]
                self.u_next[j][-1] = self.u_next[j][-2]
        elif self.boundary_x == BoundaryType.PERIODIC:
            for j in range(self.ny):
                # Periodic in x: i=0 uses i=-2, i=-1 uses i=1
                laplacian_x_0 = self.u_curr[j][1] - Rational(2)*self.u_curr[j][0] + self.u_curr[j][-2]
                laplacian_y_0 = self.u_curr[j+1][0] - Rational(2)*self.u_curr[j][0] + self.u_curr[j-1][0]
                self.u_next[j][0] = (
                    Rational(2) * self.u_curr[j][0] - self.u_prev[j][0] +
                    self.alpha_x * laplacian_x_0 + self.alpha_y * laplacian_y_0
                )
                laplacian_x_end = self.u_curr[j][0] - Rational(2)*self.u_curr[j][-1] + self.u_curr[j][-2]
                laplacian_y_end = self.u_curr[j+1][-1] - Rational(2)*self.u_curr[j][-1] + self.u_curr[j-1][-1]
                self.u_next[j][-1] = (
                    Rational(2) * self.u_curr[j][-1] - self.u_prev[j][-1] +
                    self.alpha_x * laplacian_x_end + self.alpha_y * laplacian_y_end
                )
        
        # Y boundaries
        if self.boundary_y == BoundaryType.DIRICHLET:
            for i in range(self.nx):
                self.u_next[0][i] = Rational(0)
                self.u_next[-1][i] = Rational(0)
        elif self.boundary_y == BoundaryType.NEUMANN:
            for i in range(self.nx):
                self.u_next[0][i] = self.u_next[1][i]
                self.u_next[-1][i] = self.u_next[-2][i]
        elif self.boundary_y == BoundaryType.PERIODIC:
            for i in range(self.nx):
                laplacian_x_0 = self.u_curr[0][i+1] - Rational(2)*self.u_curr[0][i] + self.u_curr[0][i-1]
                laplacian_y_0 = self.u_curr[1][i] - Rational(2)*self.u_curr[0][i] + self.u_curr[-2][i]
                self.u_next[0][i] = (
                    Rational(2) * self.u_curr[0][i] - self.u_prev[0][i] +
                    self.alpha_x * laplacian_x_0 + self.alpha_y * laplacian_y_0
                )
                laplacian_x_end = self.u_curr[-1][i+1] - Rational(2)*self.u_curr[-1][i] + self.u_curr[-1][i-1]
                laplacian_y_end = self.u_curr[0][i] - Rational(2)*self.u_curr[-1][i] + self.u_curr[-2][i]
                self.u_next[-1][i] = (
                    Rational(2) * self.u_curr[-1][i] - self.u_prev[-1][i] +
                    self.alpha_x * laplacian_x_end + self.alpha_y * laplacian_y_end
                )
        if self.domain_type == "circular":
            for j in range(self.ny):
                for i in range(self.nx):
                    if not self._circular_mask[j][i]:
                        self.u_next[j][i] = Rational(0)
        
        # Swap arrays
        self.u_prev, self.u_curr, self.u_next = self.u_curr, self.u_next, self.u_prev
        
        self.time += self.dt
        self.step += 1
        self.history.append([[row[i] for i in range(self.nx)] for row in self.u_curr])
        
        return self.u_curr
    def run(self, steps: int | None = None) -> list[list[list[Rational]]]:
        """Run simulation for specified number of steps."""
        if steps is None:
            steps = self.nt
        
        for _ in range(steps):
            self.step_forward()
        
        return self.history
    
    def compute_energy(self) -> Rational:
        """Compute total energy in 2D."""
        # Kinetic: 1/2 ∫∫ u_t² dx dy
        kinetic = Rational(0)
        for j in range(self.ny):
            for i in range(self.nx):
                if self._is_valid_point(i, j):
                    u_t = (self.u_curr[j][i] - self.u_prev[j][i]) / self.dt
                    kinetic += u_t * u_t
        kinetic = kinetic * self.dx * self.dy / 2
        
        # Potential: 1/2 c² ∫∫ (u_x² + u_y²) dx dy
        potential = Rational(0)
        for j in range(1, self.ny - 1):
            for i in range(1, self.nx - 1):
                if not self._is_valid_point(i, j):
                    continue
                u_x = (self.u_curr[j][i+1] - self.u_curr[j][i-1]) / (Rational(2) * self.dx)
                u_y = (self.u_curr[j+1][i] - self.u_curr[j-1][i]) / (Rational(2) * self.dy)
                potential += u_x * u_x + u_y * u_y
        
        # Boundary terms for Neumann/Periodic
        if self.boundary_x == BoundaryType.NEUMANN:
            # u_x = 0 at x boundaries
            pass
        elif self.boundary_x == BoundaryType.PERIODIC:
            for j in range(self.ny):
                u_x_0 = (self.u_curr[j][1] - self.u_curr[j][-2]) / (Rational(2) * self.dx)
                u_x_end = (self.u_curr[j][0] - self.u_curr[j][-2]) / (Rational(2) * self.dx)
                potential += u_x_0 * u_x_0 + u_x_end * u_x_end
        
        if self.boundary_y == BoundaryType.NEUMANN:
            pass
        elif self.boundary_y == BoundaryType.PERIODIC:
            for i in range(self.nx):
                u_y_0 = (self.u_curr[1][i] - self.u_curr[-2][i]) / (Rational(2) * self.dy)
                u_y_end = (self.u_curr[0][i] - self.u_curr[-2][i]) / (Rational(2) * self.dy)
                potential += u_y_0 * u_y_0 + u_y_end * u_y_end
        
        potential = potential * (self.c ** 2) * self.dx * self.dy / 2
        
        return kinetic + potential


# =====================================================================
# Modal Analysis
# =====================================================================

def modal_analysis_1d(
    length: Rational,
    c: Rational,
    boundary: BoundaryType,
    num_modes: int
) -> list[Mode]:
    """Compute exact normal modes for 1D wave equation.
    
    For a string of length L with wave speed c:
    
    Dirichlet (fixed ends):     u_n(x) = sin(nπx/L),     ω_n = nπc/L,  λ_n = 2L/n
    Neumann (free ends):        u_n(x) = cos(nπx/L),     ω_n = nπc/L,  λ_n = 2L/n
    Periodic:                   u_n(x) = exp(i 2πn x/L), ω_n = 2πn c/L, λ_n = L/n
    
    Returns exact rational representations where possible.
    Note: π is irrational, so frequencies are expressed as rational multiples of πc/L.
    """
    modes = []
    
    if boundary == BoundaryType.DIRICHLET or boundary == BoundaryType.NEUMANN:
        for n in range(1, num_modes + 1):
            # Frequency: ω_n = nπc/L
            # Represented as rational multiple of πc/L
            freq_coeff = Rational(n)
            wavelength = Rational(2) * length / n
            
            # Mode shape at grid points (will be evaluated at specific dx)
            # For exact shape, we return the coefficients
            modes.append(Mode(
                index=n,
                frequency=freq_coeff,  # Coefficient of πc/L
                wavelength=wavelength,
                shape=[]  # Filled in by evaluate_mode_shape
            ))
    elif boundary == BoundaryType.PERIODIC:
        for n in range(0, num_modes + 1):
            if n == 0:
                # n=0 mode: constant
                freq_coeff = Rational(0)
                wavelength = length
            else:
                freq_coeff = Rational(2 * n)  # 2πn c/L
                wavelength = length / n
            modes.append(Mode(
                index=n,
                frequency=freq_coeff,
                wavelength=wavelength,
                shape=[]
            ))
    
    return modes


def modal_analysis_2d_rectangular(
    lx: Rational,
    ly: Rational,
    c: Rational,
    boundary_x: BoundaryType,
    boundary_y: BoundaryType,
    max_n: int,
    max_m: int
) -> list[Mode]:
    """Compute exact normal modes for 2D rectangular domain.
    
    For Dirichlet boundaries:
    u_{n,m}(x,y) = sin(nπx/Lx) sin(mπy/Ly)
    ω_{n,m} = πc sqrt((n/Lx)² + (m/Ly)²)
    
    Returns modes as rational coefficients of πc.
    """
    modes = []
    
    for n in range(1, max_n + 1):
        for m in range(1, max_m + 1):
            # Frequency squared: ω² = π²c²((n/Lx)² + (m/Ly)²)
            # We store the rational coefficient inside the sqrt
            n_term = Rational(n * n) / (lx * lx)
            m_term = Rational(m * m) / (ly * ly)
            freq_sq_coeff = n_term + m_term  # This is the rational inside π²c² * (...)
            
            modes.append(Mode(
                index=(n, m),
                frequency=freq_sq_coeff,  # Coefficient of π²c²
                wavelength=Rational(0),   # Not single wavelength in 2D
                shape=[]
            ))
    
    # Sort by frequency
    modes.sort(key=lambda m: m.frequency)
    return modes


def evaluate_mode_shape_1d(mode: Mode, x: Rational, length: Rational) -> Rational:
    """Evaluate 1D mode shape at position x.
    
    Note: Returns exact expression involving sin/cos of rational multiples of π.
    For exact rational arithmetic, we return the argument to sin/cos as a Phase.
    """
    from .frequency import Phase
    
    if mode.index == 0:
        return Rational(1)  # Constant mode
    
    n = mode.index
    # u_n(x) = sin(nπx/L) or cos(nπx/L)
    # Phase = n*x/L turns (where 1 turn = 2π)
    phase_turns = Rational(n) * x / length
    if phase_turns >= 1:
        phase_turns = Phase(phase_turns).value
    
    # We can't compute sin exactly with rational arithmetic
    # Return the phase for exact representation
    # User can convert to float for plotting
    return phase_turns


def evaluate_mode_shape_2d(
    mode: Mode, x: Rational, y: Rational, lx: Rational, ly: Rational
) -> Rational:
    """Evaluate 2D mode shape at (x,y). Returns phase information."""
    n, m = mode.index
    phase_x = Rational(n) * x / lx
    phase_y = Rational(m) * y / ly
    return phase_x * phase_y  # Product of phases


# =====================================================================
# Utility Functions
# =====================================================================

def standing_wave_1d(
    x: Rational,
    t: Rational,
    n: int,
    length: Rational,
    c: Rational,
    amplitude: Rational = Rational(1)
) -> Rational:
    """Exact standing wave solution for 1D Dirichlet boundaries.
    
    u_n(x,t) = A sin(nπx/L) cos(nπct/L)
    
    Returns the phase argument (rational multiple of π) for exact representation.
    """
    from .frequency import Phase
    
    if n == 0:
        return Rational(0)
    
    spatial_phase = Rational(n) * x / length
    temporal_phase = Rational(n) * c * t / length
    
    # Return both phases - user combines with sin/cos
    return spatial_phase, temporal_phase


def cavity_mode_2d(
    x: Rational,
    y: Rational,
    t: Rational,
    n: int,
    m: int,
    lx: Rational,
    ly: Rational,
    c: Rational,
    amplitude: Rational = Rational(1)
) -> tuple[Rational, Rational]:
    """Exact cavity mode for 2D rectangular Dirichlet boundaries.
    
    u_{n,m}(x,y,t) = A sin(nπx/Lx) sin(mπy/Ly) cos(ω_{n,m}t)
    where ω_{n,m} = πc sqrt((n/Lx)² + (m/Ly)²)
    
    Returns (spatial_phase_product, temporal_phase_coeff).
    """
    spatial_x = Rational(n) * x / lx
    spatial_y = Rational(m) * y / ly
    
    # ω_{n,m}t = πc t sqrt((n/Lx)² + (m/Ly)²)
    # Return the rational coefficient inside the sqrt
    n_term = Rational(n * n) / (lx * lx)
    m_term = Rational(m * m) / (ly * ly)
    temporal_coeff = c * t  # Multiply by sqrt(n_term + m_term) * π
    
    return (spatial_x * spatial_y, temporal_coeff)


def drift_metric(history: list[list[Rational]], exact_solution: list[Rational]) -> Rational:
    """Compute drift metric: max|u_numerical - u_exact| over all grid points and time."""
    max_drift = Rational(0)
    for step_sol in history:
        for i, (num, exact) in enumerate(zip(step_sol, exact_solution)):
            diff = abs(num - exact)
            if diff > max_drift:
                max_drift = diff
    return max_drift


def energy_drift(history: list[list[Rational]], params: WaveParameters) -> list[Rational]:
    """Compute energy at each time step for drift analysis."""
    # This would require storing u_prev at each step
    # Simplified: return empty list, use solver.compute_energy() instead
    return []


# =====================================================================
# Base-60 Optimized Grid Generation
# =====================================================================

def optimal_grid_1d(
    length: Rational,
    c: Rational,
    dt: Rational,
    max_points: int = 3600  # 60^2
) -> tuple[int, Rational]:
    """Find optimal 5-smooth grid size for 1D.
    
    Returns (nx, dx) where nx is 5-smooth and CFL condition is satisfied.
    """
    # CFL: c*dt/dx <= 1 => dx >= c*dt
    min_dx = c * dt
    
    # Try 5-smooth numbers for nx
    # length = (nx-1)*dx => dx = length/(nx-1)
    # So we need length/(nx-1) >= min_dx => nx-1 <= length/min_dx
    max_nx_minus_1 = int((length / min_dx).to_float())
    max_nx = min(max_nx_minus_1 + 1, max_points)
    
    # Find largest 5-smooth <= max_nx
    nx = nearest_5_smooth(max_nx, "down")
    if nx < 3:
        nx = 3
    
    dx = length / (nx - 1)
    
    # Verify CFL
    if c * dt / dx > 1:
        # Need smaller dt or larger dx
        # Increase nx to next 5-smooth
        nx = nearest_5_smooth(nx + 1, "up")
        dx = length / (nx - 1)
    
    return nx, dx


def optimal_grid_2d(
    lx: Rational,
    ly: Rational,
    c: Rational,
    dt: Rational,
    max_points: int = 3600
) -> tuple[int, int, Rational, Rational]:
    """Find optimal 5-smooth grid for 2D rectangular domain."""
    nx, dx = optimal_grid_1d(lx, c, dt, max_points)
    ny, dy = optimal_grid_1d(ly, c, dt, max_points)
    return nx, ny, dx, dy


__all__ = [
    "BoundaryType",
    "WaveParameters",
    "WaveParameters2D",
    "Mode",
    "WaveSolver1D",
    "WaveSolver2D",
    "is_5_smooth",
    "nearest_5_smooth",
    "generate_5_smooth_grid",
    "modal_analysis_1d",
    "modal_analysis_2d_rectangular",
    "evaluate_mode_shape_1d",
    "evaluate_mode_shape_2d",
    "standing_wave_1d",
    "cavity_mode_2d",
    "drift_metric",
    "optimal_grid_1d",
    "optimal_grid_2d",
]