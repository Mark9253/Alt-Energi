# Anniversary cron setup

The `AllEnergy: Subscription Anniversary Task Scheduling` cron in
`allenergy_core` runs daily and does two things per active subscription:

1. **30 days before the next start-date anniversary** — creates a
   `project.task` on the Planned Maintenance project, dated to the
   anniversary itself.
2. **60 days before the next anniversary** — creates a `mail.activity`
   on the subscription, deadline = anniversary minus 45 days, prompting
   an admin to send the RPI+1% uplift notice required by T&Cs clause 3.4.

Both create steps are idempotent (existing matching records are left
alone), so the cron is safe to re-run manually if a daily run is missed.

## One-time setup

The cron needs to know which project the FSM tasks should land on.

1. Create the `Planned Maintenance` project (Field Service > Configuration
   > Projects, or via the Projects app). This is task 12 in the build
   sequence.
2. Settings > Technical > System Parameters.
3. Set `allenergy.planned_maintenance_project_id` to the integer ID of
   the project. The ID is in the URL when you open the project record.

Until the parameter is set, the cron logs a warning each run and skips
the FSM task creation step. The uplift notice activity step still runs.

## Manually triggering a run

Settings > Technical > Scheduled Actions > AllEnergy: Subscription
Anniversary Task Scheduling > Run Manually.
