# Powerline K8S Status

[![CodeQL](https://github.com/imjoseangel/powerline-k8sstatus/workflows/CodeQL/badge.svg)](https://github.com/imjoseangel/powerline-k8sstatus/security/code-scanning) [![codecov](https://codecov.io/gh/imjoseangel/powerline-k8sstatus/branch/devel/graph/badge.svg)](https://codecov.io/gh/imjoseangel/powerline-k8sstatus) [![Python package](https://github.com/imjoseangel/powerline-k8sstatus/workflows/Python%20package/badge.svg)](https://pypi.org/project/powerline-k8sstatus)

A [Powerline][1] segment for showing the status of current Kubernetes context.

By [imjoseangel][2]

![screenshot][4]

It will show any or all of:

* context name
* namespace
* username

You can also:

* Toggle on or off the powerline-k8sstatus segment using an environment variable which can easily be mapped to a function in your ~/.profile file.

* Define certain contexts or namespaces to be colored differently for alerting purposes. For instance, you can have your production context or kube-system namespace showing up in bright red or solarized yellow respectively.

## Requirements

The K8Sstatus segment requires [kubectl][5]. It can be installed following the instructions [here][6].

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
    "k8sstatus": {
      "fg": "brightestorange",
      "bg": "gray2",
      "attrs": []
    },
    "k8sstatus:alert": {
      "fg": "white",
      "bg": "solarized:red",
      "attrs": [
        "bold"
      ]
    },
    "k8sstatus_namespace": {
      "fg": "gray10",
      "bg": "darkestblue",
      "attrs": []
    },
    "k8sstatus_namespace:alert": {
      "fg": "darkestred",
      "bg": "solarized:yellow",
      "attrs": []
    },
    "k8sstatus_user": {
      "fg": "white",
      "bg": "green",
      "attrs": []
    },
    "k8sstatus:divider": {
      "fg": "white",
      "bg": "mediumorange",
      "attrs": []
    }
  }
}
```

Then you can activate the K8Sstatus segment by adding it to your segment configuration,
for example in `.config/powerline/themes/shell/default.json`:

```json
{
  "function": "powerline_k8sstatus.k8sstatus",
  "priority": 50,
  "args": {
    "show_namespace": true,
    "show_user": true,
    "context_alert": [
      "minikube",
      "production"
    ],
    "namespace_alert": [
      "kube-system",
      "production"
    ]
  }
}
```

* Context names added to the `context_alert` arguments will be outlined in the segment by a different colour.
* Namespace names added to the `namespace_alert` arguments will be outlined in the segment by a different colour. Note that `default` namespace won't be shown and as result not colorized.

Reload powerline running `powerline-daemon --replace` to load the new settings.

By default **powerline-k8sstatus** will display the Kubernetes status segment context. It can be disabled temporarily if the environment variable `POWERLINE_K8SSTATUS` is set to `0`. One way to do this would be with a simple function, such as putting this `k8sstatus` function in your `~/.bash_profile`:

```bash
k8sstatus() {
    if [[ $POWERLINE_K8SSTATUS = "0" ]]; then
        unset POWERLINE_K8SSTATUS
    else
        export POWERLINE_K8SSTATUS=0
    fi
}
```

Toggle showing your Kubernetes segment in powerline by just typing `k8sstatus` in your terminal

## Authors

Originally created by [@imjoseangel](http://github.com/imjoseangel)

## License

Licensed under [the MIT License][3].

[1]: https://powerline.readthedocs.org/en/master/
[2]: https://imjoseangel.github.io
[3]: https://github.com/imjoseangel/powerline-k8sstatus/blob/devel/LICENSE
[4]: https://raw.githubusercontent.com/imjoseangel/powerline-k8sstatus/devel/screenshot.png
[5]: https://kubernetes.io/docs/reference/kubectl/overview/
[6]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
