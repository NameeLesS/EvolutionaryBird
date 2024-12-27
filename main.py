from evolution import BirdEvolution

def main():
    bird_evolution = BirdEvolution()
    bird_evolution.evolve(2000, pop_size=40, p_mutation_initial=0.15, p_mutation_min=0.01, offspring_size=20)



if __name__ == '__main__':
    main()
