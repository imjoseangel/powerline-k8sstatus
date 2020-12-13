import logging
from kubernetes import config
import pytest
import powerline_k8sstatus as powerlinek8s


CONTEXT = 'minikube'
NAMESPACE = 'tools'
EXPECTED_NAMESPACE = {
    'contents': NAMESPACE,
    'highlight_groups': ['k8sstatus_namespace', 'k8sstatus'],
    'divider_highlight_group': 'k8sstatus:divider'
}


def mockk8sreturn():
    return ([{'context': {'cluster': 'minikube', 'namespace': NAMESPACE, 'user': CONTEXT}, 'name': 'minikube'}], {'context': {'cluster': 'minikube', 'namespace': NAMESPACE, 'user': 'minikube'}, 'name': CONTEXT})


def mockk8sdefaultreturn():
    return ([{'context': {'cluster': 'minikube', 'namespace': 'default', 'user': CONTEXT}, 'name': 'minikube'}], {'context': {'cluster': 'minikube', 'namespace': 'default', 'user': 'minikube'}, 'name': CONTEXT})


def mockk8snotnsreturn():
    return ([{'context': {'cluster': 'minikube', 'user': 'minikube'}, 'name': CONTEXT}], {'context': {'cluster': 'minikube', 'user': 'minikube'}, 'name': CONTEXT})


@pytest.fixture
def expected_symbol(request):
    return {'contents': (u'\U00002388 {}').format(
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
def setup_nsmocked_context(monkeypatch):
    monkeypatch.setattr(config, 'list_kube_config_contexts', mockk8sreturn)


@pytest.fixture
def setup_mocked_context(monkeypatch):
    monkeypatch.setattr(config, 'list_kube_config_contexts',
                        mockk8sdefaultreturn)


@pytest.fixture
def setup_notnsmocked_context(monkeypatch):
    monkeypatch.setattr(
        config, 'list_kube_config_contexts', mockk8snotnsreturn)


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nsmocked_context', 'expected_symbol')
def test_cluster_notnamespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nsmocked_context', 'expected_symbol')
def test_cluster_namespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='', show_namespace=True)
    assert output == [expected_symbol, EXPECTED_NAMESPACE]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_cluster_notnamespacedefault(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_cluster_notnamespacedefaulttrue(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='', show_namespace=True)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_notnsmocked_context', 'expected_symbol')
def test_cluster_notnamespacdefined(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_notnsmocked_context', 'expected_symbol')
def test_cluster_notnamespacedefinedtrue(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='', show_namespace=True)
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nsmocked_context', 'expected_symbol')
def test_envvar_notzero(pl, expected_symbol):
    segment_info = {'environ': {'POWERLINE_K8SSTATUS': '1'}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nsmocked_context', 'expected_symbol')
def test_envvar_notzeroempty(pl, expected_symbol):
    segment_info = {'environ': {}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_nsmocked_context', 'expected_symbol')
def test_envvar_zero(pl, expected_symbol):
    segment_info = {'environ': {'POWERLINE_K8SSTATUS': '0'}}
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output is None


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context')
def test_no_items(pl, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output is None
