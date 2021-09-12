#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R1710,W0621,W0613,C0301

import logging
from kubernetes import config
import pytest
import powerline_k8sstatus as powerlinek8s

CONTEXT = 'minikube'
NAMESPACE = 'tools'
USER = 'minikube'
VERSION = 'v1.22.1'

EXPECTED_NAMESPACE = {
    'contents': NAMESPACE,
    'highlight_groups': ['k8sstatus_namespace', 'k8sstatus'],
    'divider_highlight_group': 'k8sstatus:divider'
}

EXPECTED_NAMESPACE_ALERT = {
    'contents': NAMESPACE,
    'highlight_groups': ['k8sstatus_namespace:alert', 'k8sstatus'],
    'divider_highlight_group': 'k8sstatus:divider'
}

EXPECTED_USER = {
    'contents': USER,
    'highlight_groups': ['k8sstatus_user'],
    'divider_highlight_group': 'k8sstatus:divider'
}

EXPECTED_VERSION = {
    'contents': VERSION,
    'highlight_groups': ['k8sstatus_version'],
    'divider_highlight_group': 'k8sstatus:divider'
}


def mockk8sreturn():
    return ([{'context': {'cluster': 'minikube', 'namespace': NAMESPACE, 'user': USER}, 'name': CONTEXT}], {'context': {'cluster': 'minikube', 'namespace': NAMESPACE, 'user': USER}, 'name': CONTEXT})


def mockk8sdefaultreturn():
    return ([{'context': {'cluster': 'minikube', 'namespace': 'default', 'user': USER}, 'name': CONTEXT}], {'context': {'cluster': 'minikube', 'namespace': 'default', 'user': USER}, 'name': CONTEXT})


def mockk8snotnamespacereturn():
    return ([{'context': {'cluster': 'minikube', 'user': USER}, 'name': CONTEXT}], {'context': {'cluster': 'minikube', 'user': USER}, 'name': CONTEXT})


def mockk8snonereturn():
    return None


@pytest.fixture
def expected_symbol(request):
    return {'contents': ('\U00002388 {}').format(
        CONTEXT), 'highlight_groups': [request.param]}


@pytest.fixture
def pl():
    ''' Simulate the powerline logger '''
    logging.basicConfig()
    return logging.getLogger()


@pytest.fixture
def segment_info():
    return {'environ': {}}


@pytest.fixture
def setup_namespacemocked_context(monkeypatch):
    monkeypatch.setattr(config, 'list_kube_config_contexts', mockk8sreturn)


@pytest.fixture
def setup_mocked_context(monkeypatch):
    monkeypatch.setattr(config, 'list_kube_config_contexts',
                        mockk8sdefaultreturn)


@pytest.fixture
def setup_notnamespacemocked_context(monkeypatch):
    monkeypatch.setattr(
        config, 'list_kube_config_contexts', mockk8snotnamespacereturn)


@pytest.fixture
def setup_nonemocked_context(monkeypatch):
    monkeypatch.setattr(
        config, 'list_kube_config_contexts', mockk8snonereturn)
    monkeypatch.setattr(config, 'load_kube_config', mockk8snonereturn)


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_notnamespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_namespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True)
    assert output == [expected_symbol, EXPECTED_NAMESPACE]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_user(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_user=True)
    assert output == [expected_symbol, EXPECTED_USER]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_version(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_version=True)
    assert output == [expected_symbol, EXPECTED_VERSION]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_usernamespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True, show_user=True)
    assert output == [expected_symbol, EXPECTED_NAMESPACE, EXPECTED_USER]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_versionnamespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True, show_version=True)
    assert output == [expected_symbol, EXPECTED_NAMESPACE, EXPECTED_VERSION]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_context_versionusernamespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True, show_user=True,
        show_version=True)
    assert output == [expected_symbol, EXPECTED_NAMESPACE,
                      EXPECTED_USER, EXPECTED_VERSION]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_context_notnamespacedefault(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_context_notnamespacedefaulttrue(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_notnamespacemocked_context', 'expected_symbol')
def test_context_notnamespacdefined(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_notnamespacemocked_context', 'expected_symbol')
def test_context_notnamespacedefinedtrue(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_envvar_notzero(pl, expected_symbol):
    segment_info = {'environ': {'POWERLINE_K8SSTATUS': '1'}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_envvar_notzeroempty(pl, expected_symbol):
    segment_info = {'environ': {}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_envvar_zero(pl, expected_symbol):
    segment_info = {'environ': {'POWERLINE_K8SSTATUS': '0'}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output is None


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context')
def test_no_items(pl, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output is None


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nonemocked_context', 'expected_symbol')
def test_none_items(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info)
    assert output is None


@pytest.mark.parametrize('expected_symbol', ['k8sstatus:alert'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_context_defaultalert(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info,
        context_alert=['minikube'])
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_namespacemocked_context', 'expected_symbol')
def test_namespace_defaultalert(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, show_namespace=True,
        namespace_alert=['tools'])
    assert output == [expected_symbol, EXPECTED_NAMESPACE_ALERT]
