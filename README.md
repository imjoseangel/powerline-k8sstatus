# Powerline K8S Status

A [Powerline][1] segment for showing the status of current Kubernetes context.

By [imjoseangel][2]

![screenshot][4]

It will show any or all of:

* context name

You can also:

* Toggle on or off the powerline-k8sstatus segment using an environment variable which can easily be mapped to a function in your ~/.profile file.
* Define certain namespaces and/or contexts to be colored differently for alerting purposes. For instance, you can have your production namespaces or context showing up in bright red.

## Requirements

The K8Sstatus segment requires kubectl[5]. It can be installing following the instructions here[6].

## Installation

### Using pip

```txt
pip install powerline-k8sstatus
```

## Configuration

The K8Sstatus segment uses a couple of custom highlight groups. You'll need to define those groups in your colorscheme,
for example in `.config/powerline/colorschemes/default.json`:

```json
{
  "groups": {
    "k8sstatus": { "fg": "darkblue", "bg": "cyan2", "attrs": [] }
  }
}
```

Then you can activate the K8Sstatus segment by adding it to your segment configuration,
for example in `.config/powerline/themes/shell/default.json`:

```json
{
    "function": "powerline_k8sstatus.k8sstatus",
    "priority": 30
}
```

Reload powerline running `powerline-daemon --replace` to load the new settings.

## License

Licensed under [the MIT License][3].

[1]: https://powerline.readthedocs.org/en/master/
[2]: https://imjoseangel.github.io
[3]: https://github.com/imjoseangel/powerline-k8sstatus/blob/master/LICENSE
[5]: https://kubernetes.io/docs/reference/kubectl/overview/
[6]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
