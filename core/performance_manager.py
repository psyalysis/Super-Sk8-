"""Simple object pooling system for performance optimization."""

from typing import List, Type, TypeVar, Callable, Optional, Dict
import pygame

T = TypeVar('T')


class ObjectPool:
    def __init__(self, factory: Callable[[], T], initial_size: int = 10, max_size: int = 100):
        self.factory = factory
        self.max_size = max_size
        self.pool: List[T] = []
        self.active_objects: List[T] = []
        
        for _ in range(initial_size):
            self.pool.append(self.factory())
    
    def get(self) -> T:
        if self.pool:
            obj = self.pool.pop()
        else:
            obj = self.factory()
        
        self.active_objects.append(obj)
        return obj
    
    def return_object(self, obj: T):
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            
            if len(self.pool) < self.max_size:
                self.pool.append(obj)
    
    def clear(self):
        self.pool.clear()
        self.active_objects.clear()
    
    def get_stats(self) -> dict:
        return {
            'pool_size': len(self.pool),
            'active_count': len(self.active_objects),
            'max_size': self.max_size
        }


class SurfacePool:
    def __init__(self, size: tuple, initial_size: int = 5, max_size: int = 20):
        self.size = size
        self.pool: List[pygame.Surface] = []
        self.active_surfaces: List[pygame.Surface] = []
        self.max_size = max_size
        
        for _ in range(initial_size):
            surface = pygame.Surface(size, pygame.SRCALPHA)
            self.pool.append(surface)
    
    def get(self) -> pygame.Surface:
        if self.pool:
            surface = self.pool.pop()
        else:
            surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.active_surfaces.append(surface)
        return surface
    
    def return_surface(self, surface: pygame.Surface):
        if surface in self.active_surfaces:
            self.active_surfaces.remove(surface)
            
            if len(self.pool) < self.max_size:
                surface.fill((0, 0, 0, 0))
                self.pool.append(surface)
    
    def clear(self):
        self.pool.clear()
        self.active_surfaces.clear()


class PerformanceManager:
    def __init__(self):
        self.surface_pools: Dict[str, SurfacePool] = {}
        self.frame_times: List[float] = []
        self.max_frame_samples = 60
        
    def create_surface_pool(self, name: str, size: tuple, initial_size: int = 5) -> SurfacePool:
        pool = SurfacePool(size, initial_size)
        self.surface_pools[name] = pool
        return pool
    
    def get_surface(self, pool_name: str) -> Optional[pygame.Surface]:
        if pool_name in self.surface_pools:
            return self.surface_pools[pool_name].get()
        return None
    
    def return_surface(self, pool_name: str, surface: pygame.Surface):
        if pool_name in self.surface_pools:
            self.surface_pools[pool_name].return_surface(surface)
    
    def record_frame_time(self, frame_time: float):
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frame_samples:
            self.frame_times.pop(0)
    
    def get_average_fps(self) -> float:
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1000.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def get_performance_stats(self) -> dict:
        stats = {
            'average_fps': self.get_average_fps(),
            'frame_samples': len(self.frame_times),
            'surface_pools': {}
        }
        
        for name, pool in self.surface_pools.items():
            stats['surface_pools'][name] = pool.get_stats()
        
        return stats
    
    def cleanup(self):
        for pool in self.surface_pools.values():
            pool.clear()
        self.surface_pools.clear()
        self.frame_times.clear()