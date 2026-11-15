import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("employees.csv")
avg=df.groupby("department")["salary"].mean()
plt.bar(avg.index,avg.values)
for i in range(len(avg)):
    plt.text(i,avg.values[i],str(int(avg.values[i])),ha="center")

plt.title("Average salary per department")
plt.xlabel("Department") 
plt.ylabel("Average salary")
plt.savefig("bar_chart.png")
plt.close()

plt.hist(df["salary"],bins=5)
plt.title("Salary Distribution")   
plt.xlabel("Salary")
plt.ylabel("Number of Employees")
plt.savefig("histogram.png")
plt.close()

for dept in df["department"].unique():
    d=df[df["department"]==dept]
    plt.scatter(d["id"],d["salary"],label=dept)
plt.title("ID vs Salary")
plt.xlabel("ID")
plt.ylabel("Salary")
plt.legend()
plt.savefig("scatter_plot.png")
plt.close()

months=["Jan","Feb","Mar","Apr","May","Jun"]
sales=[12,15,14,18,22,25]
plt.plot(months,sales,marker="o")
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.savefig("line_chart.png")
plt.close()

print("4 charts saved")
    