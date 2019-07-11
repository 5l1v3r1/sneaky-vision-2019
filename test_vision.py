import math
import pytest


def getDistanceToTarget(
        heightDiff,
        cameraMountAngle,
        VFOV,
        targetY,
        cameraPixelHeight=300):
    '''

    Calculates distance to target using pitch angle method

    - **parameters**, **types**, **return** and **return types**::

        :param heightDiff:
        :param cameraMountAngle: Angle of the Camera Mount,
        negative if pointing downwards
        :param VFOV: Vertical FOV of the camera used in degrees,
        see it's datasheet
        :param targetY: The middle point of the target on Y axis in pixels
        :param cameraPixelHeight: Height of the camera frames in pixels
        :type heightDiff: float
        :type cameraMountAngle: float
        :type VFOV: float
        :type targetY: int
        :type cameraPixelHeight: int
        :return: distance to target
        :rtype: float

    '''

    # Pixel per a degree of vertical difference in height
    pixelPerAngle = float(cameraPixelHeight / VFOV)
    middleOfCamera = cameraPixelHeight / 2.0  # Middle of the camera in pixels
    pixelDiff = middleOfCamera - targetY  # Difference of height in pixels
    # Difference of height in angles
    angleDiff = float(pixelDiff / pixelPerAngle)
    # For a1 and a2 refer to
    # http://docs.limelightvision.io/en/latest/cs_estimating_distance.html
    a2 = math.radians(angleDiff)
    a1 = math.radians(cameraMountAngle)
    if(a1 + a2 == 0):
        return 0
    distanceToTarget = abs(heightDiff / math.tan(abs(a1 + a2)))
    return distanceToTarget


def getAngleToTarget(
        HFOV,
        targetX,
        cameraPixelWidth=300):
    '''

    Calculates angle to target using yaw angle method

    - **parameters**, **types**, **return** and **return types**::

        :param HFOV: Horizontal FOV of the camera used in degrees,
        see it's datasheet
        :param targetX:  The middle point of the target on X axis in pixels
        :param cameraPixelWidth:  Height of the camera frames in pixels
        :type VFOV: float
        :type targetY: int
        :type cameraPixelHeight: int
        :return: angle to target
        :rtype: float

    '''

    # Pixel per a degree of horizontal difference in height
    pixelPerAngle = float(cameraPixelWidth / HFOV)
    middleOfCamera = cameraPixelWidth / 2.0  # Middle of the camera in pixels
    angleDiff = targetX - middleOfCamera  # Positive is right handside
    angleToTarget = float(angleDiff / pixelPerAngle)
    return angleToTarget


def test_distance():
    assert getDistanceToTarget(
        15.0, -5.0, 64.0, 200, 300) == pytest.approx(53, 5)
    assert getDistanceToTarget(
        15.0, 0.0, 64.0, 150, 300) == 0
    assert getDistanceToTarget(
        15.0, 5.0, 64.0, 100, 300) == pytest.approx(53, 5)


def test_yawAngle():
    assert getAngleToTarget(80, 150, 300) == 0
    assert getAngleToTarget(80, 300, 300) == 40.0
    assert getAngleToTarget(80, 225, 300) == 20.0
    assert getAngleToTarget(80, 0, 300) == -40.0
