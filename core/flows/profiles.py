# Filename: profiles.py
# Module name: flow
# Description: Profile system for time-varying parameters.

"""
Profile system enabling time-varying parameter values.

Profiles define how a parameter changes over time:
- FixedProfile: constant value
- LinearProfile: linear interpolation between time points
- SteppedProfile: step function with discrete jumps

ProfileRef wraps a Profile with metadata (units, description).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ProfileType(Enum):
    """Enumeration of available profile types."""
    FIXED = "fixed"
    LINEAR = "linear"
    STEPPED = "stepped"


class Profile(ABC):
    """Abstract base class for time-varying value profiles."""

    @abstractmethod
    def value_at(self, time: float) -> float:
        """Get the value at a specific time point.

        Args:
            time: Time at which to evaluate the profile

        Returns:
            The profile value at the given time
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize profile to dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Profile:
        """Deserialize profile from dictionary."""
        pass


class FixedProfile(Profile):
    """Profile with a constant value across all time."""

    def __init__(self, value: float):
        """Initialize with a fixed value.

        Args:
            value: The constant value
        """
        self.value = value

    def value_at(self, time: float) -> float:
        """Return the fixed value regardless of time."""
        return self.value

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "type": ProfileType.FIXED.value,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FixedProfile:
        """Deserialize from dictionary."""
        return cls(value=data["value"])

    def __repr__(self) -> str:
        return f"FixedProfile({self.value})"


class LinearProfile(Profile):
    """Profile with linear interpolation between time points."""

    def __init__(self, time_points: list[float], values: list[float]):
        """Initialize with time points and corresponding values.

        Args:
            time_points: List of time values (must be sorted ascending)
            values: List of values at each time point (same length as time_points)

        Raises:
            ValueError: If lengths don't match or time_points not ascending
        """
        if len(time_points) != len(values):
            raise ValueError("time_points and values must have same length")
        if len(time_points) < 2:
            raise ValueError("LinearProfile requires at least 2 points")
        if sorted(time_points) != list(time_points):
            raise ValueError("time_points must be sorted in ascending order")

        self.time_points = list(time_points)
        self.values = list(values)

    def value_at(self, time: float) -> float:
        """Linear interpolation to get value at given time.

        Returns the value at the time point if exact match,
        interpolates linearly between adjacent points,
        or returns edge value if outside range.
        """
        # Clamp to bounds
        if time <= self.time_points[0]:
            return self.values[0]
        if time >= self.time_points[-1]:
            return self.values[-1]

        # Find surrounding points
        for i in range(len(self.time_points) - 1):
            t1, t2 = self.time_points[i], self.time_points[i + 1]
            v1, v2 = self.values[i], self.values[i + 1]

            if t1 <= time <= t2:
                # Linear interpolation
                fraction = (time - t1) / (t2 - t1)
                return v1 + fraction * (v2 - v1)

        # Should not reach here due to bounds check
        return self.values[-1]

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "type": ProfileType.LINEAR.value,
            "time_points": self.time_points,
            "values": self.values,
        }

    @classmethod
    def from_dict(cls, data: dict) -> LinearProfile:
        """Deserialize from dictionary."""
        return cls(
            time_points=data["time_points"],
            values=data["values"],
        )

    def __repr__(self) -> str:
        return f"LinearProfile({len(self.time_points)} points)"


class SteppedProfile(Profile):
    """Profile with step function (constant within intervals)."""

    def __init__(self, time_points: list[float], values: list[float]):
        """Initialize with time points and step values.

        Args:
            time_points: List of time values where steps occur (must be sorted)
            values: List of values for each step (same length as time_points)

        Raises:
            ValueError: If lengths don't match or time_points not ascending
        """
        if len(time_points) != len(values):
            raise ValueError("time_points and values must have same length")
        if len(time_points) < 1:
            raise ValueError("SteppedProfile requires at least 1 point")
        if sorted(time_points) != list(time_points):
            raise ValueError("time_points must be sorted in ascending order")

        self.time_points = list(time_points)
        self.values = list(values)

    def value_at(self, time: float) -> float:
        """Get the step value at given time.

        Returns the value of the last step whose time_point is <= time.
        """
        if time < self.time_points[0]:
            # Before first step - return first value or 0
            return 0.0

        current_value = self.values[0]
        for i in range(len(self.time_points)):
            if time >= self.time_points[i]:
                current_value = self.values[i]
            else:
                break

        return current_value

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "type": ProfileType.STEPPED.value,
            "time_points": self.time_points,
            "values": self.values,
        }

    @classmethod
    def from_dict(cls, data: dict) -> SteppedProfile:
        """Deserialize from dictionary."""
        return cls(
            time_points=data["time_points"],
            values=data["values"],
        )

    def __repr__(self) -> str:
        return f"SteppedProfile({len(self.time_points)} steps)"


@dataclass
class ProfileRef:
    """Reference to a profile with metadata.

    Wraps a Profile with units and description information,
    allowing the same profile logic to be used with different units.
    """
    profile: Profile
    units: str = ""
    description: str = ""

    def value_at(self, time: float) -> float:
        """Delegate to wrapped profile's value_at method."""
        return self.profile.value_at(time)

    def to_dict(self) -> dict:
        """Serialize to dictionary including profile."""
        return {
            "profile": self.profile.to_dict(),
            "units": self.units,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ProfileRef:
        """Deserialize from dictionary."""
        # Reconstruct profile based on type
        profile_data = data["profile"]
        profile_type = profile_data.get("type")

        if profile_type == ProfileType.FIXED.value:
            profile = FixedProfile.from_dict(profile_data)
        elif profile_type == ProfileType.LINEAR.value:
            profile = LinearProfile.from_dict(profile_data)
        elif profile_type == ProfileType.STEPPED.value:
            profile = SteppedProfile.from_dict(profile_data)
        else:
            raise ValueError(f"Unknown profile type: {profile_type}")

        return cls(
            profile=profile,
            units=data.get("units", ""),
            description=data.get("description", ""),
        )
