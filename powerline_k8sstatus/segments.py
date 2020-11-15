# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division,
                        absolute_import, print_function)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info, requires_filesystem_watcher
from kubernetes import config


@requires_filesystem_watcher
@requires_segment_info
class K8SStatusSegment(Segment):
    divider_highlight_group = None

    def build_segments(self, context, namespace):
        segments = [{'contents': (u'\U00002388 {}').format(
            context), 'highlight_groups': ['k8sstatus']}]

        if namespace and namespace.lower() != 'default':
            segments.append({
                'contents': namespace,
                'highlight_groups': ['k8sstatus_namespace', 'k8sstatus'],
                'divider_highlight_group': 'k8sstatus:divider'
            })

        return segments

    def __call__(self, pl, segment_info, create_watcher, show_namespace=False):

        try:
            contexts, active_context = config.list_kube_config_contexts()
        except config.config_exception.ConfigException:
            return

        if not contexts:
            return

        context = active_context['name']

        if show_namespace:
            try:
                namespace = active_context['context']['namespace']
            except KeyError:
                namespace = 'default'
        else:
            namespace = 'default'

        return self.build_segments(context, namespace)


k8sstatus = with_docstring(
    K8SStatusSegment(), '''Return the status of the current Kubernetes context.''')
