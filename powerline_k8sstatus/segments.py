# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info
from kubernetes import config


@requires_segment_info
class K8SStatusSegment(Segment):

    def build_segments(self):
        pass

    def __call__(self, pl, segment_info, show_cluster=False, show_user=False, show_namespace=True):

        try:
            contexts, active_context = config.list_kube_config_contexts()
        except config.config_exception.ConfigException:
            return

        if not contexts:
            return

        name = active_context['name']
        cluster = active_context['context']['cluster']
        user = active_context['context']['user']

        try:
            namespace = active_context['context']['namespace']
        except KeyError:
            return

        return self.build_segments(active_context)


k8sstatus = with_docstring(K8SStatusSegment(),
                           '''Return the status of the current Kubernetes context.
It will show the context name together with the cluster name and the namespace.
:param bool show_cluster:
    Show cluster name. False by default to avoid long names.
:param bool show_namespace:
    Show namespace. True if namespace is not `default`.
:param bool show_user:
    Show cluster connected user. False by default.
Divider highlight group used: ``k8sstatus:divider``.
Highlight groups used: ``k8sstatus_name``, ``k8sstatus_cluster``, ``k8sstatus_namespace``, ``k8sstatus_user``, ``k8sstatus``.
''')
