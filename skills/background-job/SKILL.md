---
name: background-job
description: Standard workflow for running long system tasks asynchronously, polling progress, and handling crashes cleanly.
metadata:
  opencode/autoinvoke: "true"
---

## Rules for Long-Running Tasks
1. Never execute heavy background scripts or installers directly in the foreground.
2. Launch background jobs using `nohup <command> > /tmp/<job_name>.log 2>&1 & echo $! > /tmp/<job_name>.pid`.
3. Check status using `kill -0 $(cat /tmp/<job_name>.pid)` and read `/tmp/<job_name>.log`.
4. If the PID is no longer running, inspect the log file to verify whether it completed successfully or crashed.
5. Never loop or poll in a tight while-loop; always include an explicit delay between checks (e.g., `sleep 10`).
6. For long commands, direct stdout/stderr to `/tmp/logs` and exit the foreground process immediately.
7. Execute background processes using subshells that trap the EXIT signal to kill orphaned child processes automatically:
   ```bash
   (trap 'kill 0' EXIT; nohup your_command > /tmp/task.log 2>&1 & echo $! > /tmp/task.pid)
   ```
