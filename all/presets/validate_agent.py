from all.logging import DummyWriter
from all.experiments import SingleEnvExperiment, ParallelEnvExperiment

class TestSingleEnvExperiment(SingleEnvExperiment):
    def _make_writer(self, agent_name, env_name, write_loss):
        return DummyWriter()

class TestParallelEnvExperiment(ParallelEnvExperiment):
    def _make_writer(self, agent_name, env_name, write_loss):
        return DummyWriter()

def validate_agent(agent, env):
    if isinstance(agent, tuple):
        experiment = TestParallelEnvExperiment(agent, env, quiet=True)
    else:
        experiment = TestSingleEnvExperiment(agent, env, quiet=True)
    experiment.train(episodes=2)
    experiment.test(episodes=2)
