import smbus2
import time
import math

# MPU6050 Registers and Address
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# I2C Bus
bus = smbus2.SMBus(1)

# Wake up MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def get_accel_data():
    ax = read_raw_data(ACCEL_XOUT_H)
    ay = read_raw_data(ACCEL_XOUT_H + 2)
    az = read_raw_data(ACCEL_XOUT_H + 4)
    return ax, ay, az

def get_gyro_data():
    gx = read_raw_data(GYRO_XOUT_H)
    gy = read_raw_data(GYRO_XOUT_H + 2)
    gz = read_raw_data(GYRO_XOUT_H + 4)
    return gx, gy, gz

def calculate_angle(ax, ay, az):
    ax_g = ax / 16384.0
    ay_g = ay / 16384.0
    az_g = az / 16384.0

    pitch = math.degrees(math.atan2(ax_g, math.sqrt(ay_g**2 + az_g**2)))
    roll = math.degrees(math.atan2(ay_g, math.sqrt(ax_g**2 + az_g**2)))

    return pitch, roll

def main():
    print("Reading data from MPU6050...")
    try:
        while True:
            ax, ay, az = get_accel_data()
            gx, gy, gz = get_gyro_data()
            pitch, roll = calculate_angle(ax, ay, az)

            print(f"Accel: ax={ax}, ay={ay}, az={az}")
            print(f"Gyro:  gx={gx}, gy={gy}, gz={gz}")
            print(f"Angle: Pitch={pitch:.2f}°, Roll={roll:.2f}°\n")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExiting.")
