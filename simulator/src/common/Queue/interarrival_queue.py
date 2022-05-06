from src.simulator.generators.exponential_generator import ExponentialGenerator

import src.common.EsiCodes.esi_constants as esi_const


class InterarrivalQueue:
    def __init__(self):
        self.generators = [ExponentialGenerator(
            rate) for rate in esi_const.ESI_RATES]

        self.samples = [
            [esi_code, self.generators[esi_code - 1].generate_sample()]
            for esi_code in esi_const.ESI_CODES
        ]

        self.reorder_samples()

    def reorder_samples(self):
        self.samples = sorted(self.samples, key=lambda x: x[1])

    def peek(self):
        # Return the minimum
        return self.samples[0]

    def pop_regenerate_decrement_others(self):
        # Return the minimum, update the sample that I do not return,
        # regenerate the new sample for its esi code
        return_value = self.samples[0]

        # Pull
        decrement_amount = return_value[1]
        self.samples = [[s[0], s[1] - decrement_amount]
                        for s in self.samples[1:]]

        esi_code_to_regenerate = return_value[0]

        # Push
        self.samples.append([
            esi_code_to_regenerate,
            self.generators[esi_code_to_regenerate - 1].generate_sample()
        ])

        self.reorder_samples()

        return return_value

    def decrement_interarrive(self, decrement_amount):
        for sample in self.samples:
            sample[1] -= decrement_amount


if __name__ == '__main__':
    my_interarrival_queue = InterarrivalQueue()

    print('Initial values: ', my_interarrival_queue.samples)

    print('Peek value: ', my_interarrival_queue.peek())
    print('Pop and regenerate value: ',
          my_interarrival_queue.pop_regenerate_decrement_others())

    print('Values after pop and regenerate: ', my_interarrival_queue.samples)
