document.addEventListener("DOMContentLoaded", () => {
  if (!window.dashboardData) {
    return;
  }

  const ctx = document.getElementById("usageChart");
  if (!ctx) {
    return;
  }

  const labels = window.dashboardData.labels.map((label) => {
    // Try to format ISO timestamps to a more readable form.
    try {
      const date = new Date(label);
      return date.toLocaleString();
    } catch {
      return label;
    }
  });

  new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Energy Usage",
          data: window.dashboardData.values,
          borderColor: "rgba(0, 176, 255, 0.9)",
          backgroundColor: "rgba(0, 176, 255, 0.18)",
          borderWidth: 3,
          tension: 0.33,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            color: "rgba(245, 247, 255, 0.82)",
          },
          grid: {
            display: false,
          },
        },
        y: {
          ticks: {
            color: "rgba(245, 247, 255, 0.82)",
          },
          grid: {
            color: "rgba(255, 255, 255, 0.08)",
          },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: "rgba(245, 247, 255, 0.85)",
          },
        },
        tooltip: {
          backgroundColor: "rgba(10, 17, 32, 0.92)",
          titleColor: "#fff",
          bodyColor: "#f5f7ff",
          borderColor: "rgba(255, 255, 255, 0.15)",
          borderWidth: 1,
        },
      },
    },
  });
});
