Poe the Poet Tasks
==================

_Task packages_ are a construct in Poe the Poet that allows tasks to be included from a python package. This library provides primitives to support defining poe tasks in python, as well as an opinionated collection of tasks ready for inclusion in your projects.

Compatiable with Poe the Poet version >= 0.34.0

## Usage

### Using tasks

This library defines an opinionated collection of tasks that you can add to your project by adding a dev dependency on `poethepoet-tasks`, and including the following line in your _pyproject.toml_.

```toml
[tool.poe]
task_packages = "poethepoet_tasks:tasks"
```

Note that available tasks may change from one release to the next so it is recommended to depend on a specific version so that the tasks in your project don't change unexpectedly.

#### Selecting tasks using tags

By default all available tasks are loaded, but you can also optionally specify a list of tags to include (in which case only matching tags are included), as well as a list of tags to exclude. Exclusion has higher logical precedence than inclusion.

For example, by default the *format* task applies both ruff and black formatters. However if you want to simplify things you can exclude all tasks tagged with 'black', and then you'll only get ruff based formatting and linting.

```toml
task_packages = "poethepoet_tasks.tasks:tasks(exclude_tags=['black'])"
```

As another example you could include only the test task like so:

```toml
task_packages = "poethepoet_tasks.tasks:tasks(exclude_tags=['test-task'])"
```

#### Configuring tasks

Tasks that use [ruff](https://docs.astral.sh/ruff/) come with an opinionated config file that'll work well for most projects. However if you want to provide your own config you can do so by setting `$RUFF_CONFIG` like so:

```toml
[tool.poe]
env = { RUFF_CONFIG = "path/to/ruff.toml" }
task_packages = "poethepoet_tasks:tasks"
```

See the section below on Mixing task collections for an alternative approach of customizing tasks from a tasks package like this one.

### Defining your own tasks

The TaskCollection class provides a powerful abstraction for declaring poe tasks in code, to create task packages for reuse across multiple projects. It also provides a way to unify the declaration and definition of script tasks.

See the [Poe the Poet documentation](https://poethepoet.natn.io/tasks/index.html) for details on how to configure different kinds of tasks.

Given the following file at `src/tasks.py`

```python
from poethepoet_tasks import TaskCollection

tasks = TaskCollection()

# Define a simple cmd task
tasks.add(
    task_name="test",
    task_config={
        "help": "Run project tests",
        "cmd": "pytest tests",
    },
    tags=["pytest"], # tags are optional and allow consumers to select only the desired tasks
)
```

Now we can load these tasks by including the following in our `pyproject.toml`:

```toml
[tool.poe]
task_packages = "tasks:tasks()"
```

Here's we're loading tasks from a package within the same repo, but as with script tasks, any package within the environment used by poe can be a source of tasks.

A TaskCollection may define multiple versions of the same task, in which case the first one to match the specified tags is used.

All tasks are tagged with `f"task-{task_name}"` by default.

See the tasks package in this repo for a [real world example](https://github.com/nat-n/poethepoet-tasks/blob/main/src/poethepoet_tasks/tasks.py).

## Configuring environment variables for tasks

...

## Inline script tasks

The TaskCollection object also provides a decorator to be applied directly to python functions to declare them as script tasks.

```python
from poethepoet_tasks import TaskCollection

tasks = TaskCollection()

@tasks.script(task_args=True)
def hello( # The function name will be taken as the task name by default
    foo: str | None = None,
    *, # This means previous args will be positional, instead of CLI options
    bar: int = 1, # this optional argument will be parsed to an integer
    baz: bool = 1.0, # this optional argument will be a CLI flag
):
    """
    The function docstring is picked up as the task help message!
    """
    pass
```

The `script` decorator registers a new script task in the TaskCollection. It accepts the following optional keyword arguments as configuration:

- **task_name** `str`: The name of the task. if not set then the function name is used (in kebab-case).
- **help** `str`: Documentation to display for this task. If not set then the function docstring is used.
- **task_args** `bool`: Set to true to enable automatic configuration of task args from the function signature.
- **options** `dict`: Any [other options](https://poethepoet.natn.io/tasks/task_types/script.html#available-task-options) to provide as config for the script task.
- **tags** `Collection[str]`: A collection of tags to associate with this item in the task collection.

## Mixing task collections

You may wish to extend or modify a third party TaskCollection (such as this one) when creating your own.

You can import and modify an existing TasksCollection in your own package like so:

```python
from poethepoet_tasks import tasks

# Remove all definitions for the check task
tasks.remove("check")

# Define a new "check" task without tests this time
tasks.add(
    task_name="check",
    task_config={
        "help": "Run all checks on the code base",
        "sequence": ["lint", "types"],
    },
    tags=["lint", "ruff", "types"],
)
```

You can also an imported TaskCollection into your own:

```python
from poethepoet_tasks import TaskCollection, tasks

my_tasks = TaskCollection()

tasks.add(task_name="build", ...)

# Include all tasks from poethepoet_tasks with lower precedence that tasks added to
# my_tasks so far
my_tasks.include(tasks)
```

Poe the Poet allows multiple task packages to be configured, however this comes with some performance cost (especially in poetry based projects). Each loaded task package requires a python subprocess to evaluate (even for tab completion) so merging TaskCollections can help with this.
