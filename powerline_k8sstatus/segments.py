# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info
from kubernetes import config


@requires_segment_info
class K8SStatusSegment(Segment):

    def build_segments(self, formats, context):
        segments = [
            {'contents': formats.get('k8sstatus', u'\U00002388  {}').format(
                context), 'divider_highlight_group': 'k8sstatus:divider'}
        ]

        return segments

    def __call__(self, pl, segment_info, formats={}):

        try:
            contexts, active_context = config.list_kube_config_contexts()
        except config.config_exception.ConfigException:
            return

        if not contexts:
            return

        context = active_context['name']

        return self.build_segments(formats, context)


k8sstatus = with_docstring(K8SStatusSegment(),
'''Return the status of the current Kubernetes context.

It will show the context name together with the cluster name and the namespace.

:param dict formats:
    A string-to-string dictionary for customizing K8S status formats. Valid keys include ``context``.
    Empty dictionary by default, which means the default formats are used.

Divider highlight group used: ``k8sstatus:divider``.

Highlight groups used: ``k8sstatus_name``, ``k8sstatus``.
''')
