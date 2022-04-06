from simulator.src.simulator.generators.exponential_generator import ExponentialGenerator

import simulator.src.common.ColorCode.color_constants as color_constants


class InterarrivalQueue:
    def __init__(self):
        self.generators = [ExponentialGenerator(
            rate) for rate in color_constants.COLOR_RATES]

        self.samples = [
            [color_index, self.generators[color_index].generate_sample()]
            for color_index in color_constants.COLORS
        ]

        self.reorder_samples()

    def reorder_samples(self):
        self.samples = sorted(self.samples, key=lambda x: x[1])

    def peek(self):
        # Return the minimum
        return self.samples[0]

    def pop_regenerate_decrement_others(self):
        # Return the minimum, update the sample that I do not return,
        # regenerate the new sample for its color code
        return_value = self.samples[0]

        # Pull
        decrement_amount = return_value[1]
        self.samples = [[s[0], s[1] - decrement_amount]
                        for s in self.samples[1:]]

        color_code_to_regenerate = return_value[0]

        # Push
        self.samples.append([
            color_code_to_regenerate,
            self.generators[color_code_to_regenerate].generate_sample()
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
