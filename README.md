# lunch-bot

Managing lunch plans at the [Recurse Center](https://recurse.com) (RC)! At the time of development RC uses a bunch of laminated pieces of paper to plan lunch groups. We thought: "Hey, we're all programmers, why are we _getting out of our chairs_ and like, _using physical media_ when we could type on [Zulip](https://zulip.com/) instead?" Lunch Bot solves that problem!

## Interface

There's a really high chance that this README isn't updated when we add new features (you know how it do), so if you're using Lunch Bot, then please just use the `help` command.

The available commands are:

* `help` - Displays all available commands that Lunch Bot understands

* `make-plan [restaurant] [time]` - Creates a lunch plan for a given place and time. [restaurant] and [time] must not contain any spaces.

*  `show-plans` -  Shows all active lunch plans along with their associated lunch_id

* `rsvp [lunch_id]` - RSVPs to a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command.

* `my-plans` - Shows all lunch plans you have currently RSVP'd to.

* `un-rsvp [lunch_id]` - Removes your RSVP from a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command.

* `delete-plan [lunch_id]` - Deletes a certain lunch plan, given its [lunch_id]. To see every lunch_id, use the show-plans command.

## Contributing

If you're interested in contributing to Lunch Bot: great! We only have one request: use [pre-commit](https://pre-commit.com/). Once it's set up, it will run [black](https://github.com/psf/black) and [mypy](http://mypy-lang.org/) every time to commit.

```bash
# Install pre-commit
$ brew install pre-commit # On mac
$ pip install pre-commit # Everywhere else

# Register pre-commit in the repo
$ pre-commit install
```

## License

MIT licensed. Refer to `LICENSE` document.
