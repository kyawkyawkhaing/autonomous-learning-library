import numpy as np
import torch
import numbers

class State(dict):
    def __init__(self, x, device='cpu'):
        if not 'observation' in x:
            raise Exception('State must contain an observation')
        if not 'reward' in x:
            x['reward'] = 0
        if not 'done' in x:
            x['done'] = False
        if not 'mask' in x:
            x['mask'] = 1 - x['done']
        super().__init__(x)
        self.device = device

    def from_list(self, states):
        d = {}
        for key in self.keys():
            d[key] = [state[key] for state in states]
        return State(d)

    def __getitem__(self, key):
        if isinstance(key, int):
            return # TODO
        value = super().__getitem__(key)
        if torch.is_tensor(value):
            return value
        if isinstance(value, list):
            if torch.is_tensor(value[0]):
                return torch.cat(value)
            if isinstance(value[0], numbers.Number):
                return torch.tensor(value, device=self.device)
        return value

    @classmethod
    def from_gym(cls, state, device='cpu', dtype=np.float32):
        if not isinstance(state, tuple):
            return State({
                'observation': torch.from_numpy(
                    np.array(
                        state,
                        dtype=dtype
                    )
                ).unsqueeze(0).to(device)
            })

        observation, reward, done, info = state
        observation = torch.from_numpy(
            np.array(
                observation,
                dtype=dtype
            )
        ).unsqueeze(0).to(device)
        # mask = DONE.to(device) if done else NOT_DONE.to(device)
        print(info)
        return State({
            'observation': observation,
            'reward': reward,
            'done': done,
            'info': info
        })

    @property
    def observation(self):
        return self['observation']

    @property
    def reward(self):
        return self['reward']

    @property
    def mask(self):
        return self['mask']

    @property
    def info(self):
        return self['info']

    @property
    def done(self):
        return self['done']

    def __get__(self, idx):
        if isinstance(idx, slice):
            return State(
                self._raw[idx],
                self._mask[idx],
                self._info[idx]
            )
        if isinstance(idx, torch.Tensor):
            return State(
                self._raw[idx],
                self._mask[idx],
                # can't copy info
            )
        return State(
            self._raw[idx].unsqueeze(0),
            self._mask[idx].unsqueeze(0),
            [self._info[idx]]
        )

    def __len__(self):
        return len(self._raw)

DONE = torch.tensor(
    [0],
    dtype=torch.uint8,
)

NOT_DONE = torch.tensor(
    [1],
    dtype=torch.uint8,
)
