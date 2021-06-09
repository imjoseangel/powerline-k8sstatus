#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R1710

from __future__ import (unicode_literals, division,
                        absolute_import, print_function)

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info, requires_filesystem_watcher
from kubernetes import config


@requires_filesystem_watcher
@requires_segment_info
class K8SStatusSegment(Segment):
    divider_highlight_group = None

    @staticmethod
    def build_segments(context, namespace, user, contextalert):
        segments = [{'contents': (u'\U00002388 {}').format(
            context), 'highlight_groups': [contextalert]}]

        if namespace and namespace.lower() != 'default':
            segments.append({
                'contents': namespace,
                'highlight_groups': ['k8sstatus_namespace', contextalert],
                'divider_highlight_group': 'k8sstatus:divider'
            })

        if user and user.lower():
            segments.append({
                'contents': user,
                'highlight_groups': ['k8sstatus_user'],
                'divider_highlight_group': 'k8sstatus:divider'
            })

        return segments

    def __call__(self, pl, segment_info, create_watcher=None, context_alert: list = None,
                 show_namespace=False, show_user=False):

        if context_alert is None:
            context_alert = []

        try:
            if segment_info['environ'].get('POWERLINE_K8SSTATUS') == "0":
                return
        except TypeError:
            return

        try:
            contexts, active_context = config.list_kube_config_contexts()
        except TypeError:
            return
        except config.config_exception.ConfigException:
            return

        if not contexts:
            return

        context = active_context['name']
        contextstatus = "k8sstatus"

        if context in context_alert:
            contextstatus = "k8sstatus:alert"

        if show_namespace:
            try:
                namespace = active_context['context']['namespace']
            except KeyError:
                namespace = 'default'
        else:
            namespace = 'default'

        if show_user:
            user = active_context['context']['user']
        else:
            user = None

        return self.build_segments(context, namespace, user, contextstatus)


k8sstatus = with_docstring(
    K8SStatusSegment(), '''Return the status of the current Kubernetes context.''')
