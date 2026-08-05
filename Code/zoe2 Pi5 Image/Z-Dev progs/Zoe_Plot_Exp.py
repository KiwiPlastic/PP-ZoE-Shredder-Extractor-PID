import matplotlib.pyplot as plt
import numpy as np

# Initialize PID controller
setpoint = 100  # Desired temperature
pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=setpoint)
# Simulation parameters
time = np.linspace(0, 10, 100)  # 10 seconds, 100 steps
dt = time[1] - time[0]
process_variable = 20  # Initial temperature
process_values = []
# Simulate the process
for t in time:
    # PID control output
    control_output = pid.compute(process_variable, dt)
    
    # Simulate process dynamics (heating rate proportional to control output)
    process_variable += control_output * dt - 0.1 * (process_variable - 20) * dt  # Heat loss
    
    # Store the process variable
    process_values.append(process_variable)
# Plot results
plt.figure(figsize=(10, 6))
plt.plot(time, process_values, label='Process Variable (Temperature)')
plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
plt.xlabel('Time (s)')
plt.ylabel('Temperature')
plt.title('PID Controller Simulation')
plt.legend()
plt.grid()
plt.show()