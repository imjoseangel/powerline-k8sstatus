import logging
from kubernetes import config
import pytest
import powerline_k8sstatus as powerlinek8s


EXPECTED_CONTEXT = 'mycontext'
EXPECTED_NAMESPACE = {
    'contents': 'namespace',
    'highlight_groups': ['k8sstatus_namespace', 'k8sstatus'],
    'divider_highlight_group': 'k8sstatus:divider'
}


def mockk8sreturn():
    return ([{'context': {'cluster': 'mycluster', 'user': 'myuser'}, 'name': 'mycontext'}], {'context': {'cluster': 'mycluster', 'user': 'myuser'}, 'name': 'mycontext'})


@pytest.fixture
def expected_symbol(request):
    return {'contents': (u'\U00002388 {}').format(
        EXPECTED_CONTEXT), 'highlight_groups': [request.param]}


@pytest.fixture
def pl():
    ''' Simulate the powerline logger '''
    logging.basicConfig()
    return logging.getLogger()


@pytest.fixture
def segment_info():
    return {'environ': {}}


@pytest.fixture
def setup_mocked_context(monkeypatch):
    monkeypatch.setattr(config, 'list_kube_config_contexts', mockk8sreturn)


@pytest.mark.parametrize('expected_symbol', ['k8sstatus'], indirect=True)
@pytest.mark.usefixtures('setup_mocked_context', 'expected_symbol')
def test_cluster_namespace(pl, segment_info, expected_symbol):
    output = powerlinek8s.k8sstatus(
        pl=pl, segment_info=segment_info, create_watcher='')
    assert output == [expected_symbol]
