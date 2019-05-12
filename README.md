# TaskWarrior UI that integrates the Pomodoro technique

This (basic) Qt application combines the [Pomodoro technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) with the [TaskWarrior](https://taskwarrior.org/) task manager. It is recommended that [TimeWarrior](https://taskwarrior.org/docs/timewarrior/) is also installed (incl. the [`on-modify` hook](https://taskwarrior.org/docs/timewarrior/taskwarrior.html)).

Additionally, it provides the ability to automatically enter Do-Not-Disturb mode in Slack when starting a task. To enable this feature, provide your Slack token via a configuration file in `~/.taskwpomo`:
```
slack-token: <YOUR SLACK TOKEN>
```

