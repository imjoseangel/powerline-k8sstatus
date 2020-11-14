# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info
from kubernetes.config import kube_config


@requires_segment_info
class K8SStatusSegment(Segment):
    pass


k8sstatus = with_docstring(K8SStatusSegment(),
                           '''Return the status of the current Kubernetes context.
It will show the context name together with the cluster name and the namespace.
:param bool show_cluster:
    Show cluster name. False by default to avoid long names.
:param bool show_namespace:
    Show namespace. For default namespace it hiddes the name. True if namespace is not default.
Divider highlight group used: ``k8sstatus:divider``.
Highlight groups used: ``k8sstatus_cluster``, ``k8sstatus_namespace``, ``k8sstatus``.
''')
