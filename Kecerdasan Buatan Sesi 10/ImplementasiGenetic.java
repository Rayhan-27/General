import java.util.*;

public class ImplementasiGenetic {

    static String[] teachers = {"Guru A", "Guru B", "Guru C"};
    static String[] subjects = {"Matematika", "Fisika", "Kimia"};
    static String[] classes = {"Kelas 1", "Kelas 2", "Kelas 3"};
    static String[] timeslots = {"Senin P1", "Senin P2", "Selasa P1", "Selasa P2"};

    static Random random = new Random();

    static class Individual {
        String teacher;
        String subject;
        String kelas;
        String timeslot;

        public Individual(String teacher, String subject,
                          String kelas, String timeslot) {
            this.teacher = teacher;
            this.subject = subject;
            this.kelas = kelas;
            this.timeslot = timeslot;
        }

        @Override
        public String toString() {
            return "[" + teacher + ", " + subject + ", "
                    + kelas + ", " + timeslot + "]";
        }
    }

    // Membuat individu secara acak
    static Individual createIndividual() {
        return new Individual(
                teachers[random.nextInt(teachers.length)],
                subjects[random.nextInt(subjects.length)],
                classes[random.nextInt(classes.length)],
                timeslots[random.nextInt(timeslots.length)]
        );
    }

    // Fungsi fitness
    static int fitness(Individual individual,
                       List<Individual> schedule) {

        int conflicts = 0;

        for (Individual item : schedule) {

            // Bentrok kelas dan waktu
            if (individual.kelas.equals(item.kelas)
                    && individual.timeslot.equals(item.timeslot)) {
                conflicts++;
            }

            // Bentrok guru dan waktu
            if (individual.teacher.equals(item.teacher)
                    && individual.timeslot.equals(item.timeslot)) {
                conflicts++;
            }
        }

        return conflicts;
    }

    // Seleksi 2 individu terbaik
    static List<Individual> selection(
            List<Individual> population,
            List<Individual> schedule) {

        population.sort(
                Comparator.comparingInt(
                        ind -> fitness(ind, schedule))
        );

        return population.subList(0, 2);
    }

    // Crossover
    static Individual crossover(
            Individual parent1,
            Individual parent2) {

        int point = random.nextInt(3) + 1;

        String teacher =
                (point > 0) ? parent1.teacher : parent2.teacher;

        String subject =
                (point > 1) ? parent1.subject : parent2.subject;

        String kelas =
                (point > 2) ? parent1.kelas : parent2.kelas;

        String timeslot = parent2.timeslot;

        return new Individual(
                teacher,
                subject,
                kelas,
                timeslot
        );
    }

    // Mutasi
    static void mutate(Individual individual) {

        int point = random.nextInt(4);

        switch (point) {
            case 0:
                individual.teacher =
                        teachers[random.nextInt(teachers.length)];
                break;

            case 1:
                individual.subject =
                        subjects[random.nextInt(subjects.length)];
                break;

            case 2:
                individual.kelas =
                        classes[random.nextInt(classes.length)];
                break;

            case 3:
                individual.timeslot =
                        timeslots[random.nextInt(timeslots.length)];
                break;
        }
    }

    public static void main(String[] args) {

        int populationSize = 10;
        int generations = 20;

        List<Individual> population = new ArrayList<>();

        for (int i = 0; i < populationSize; i++) {
            population.add(createIndividual());
        }

        List<Individual> schedule = new ArrayList<>();

        for (int generation = 0; generation < generations; generation++) {

            List<Individual> newPopulation = new ArrayList<>();

            for (int i = 0; i < populationSize / 2; i++) {

                List<Individual> parents =
                        selection(population, schedule);

                Individual child1 =
                        crossover(parents.get(0), parents.get(1));

                Individual child2 =
                        crossover(parents.get(1), parents.get(0));

                mutate(child1);
                mutate(child2);

                newPopulation.add(child1);
                newPopulation.add(child2);
            }

            population = newPopulation;

            Individual best =
                    Collections.min(
                            population,
                            Comparator.comparingInt(
                                    ind -> fitness(ind, schedule))
                    );

            schedule.add(best);

            System.out.println(
                    "Generasi " + (generation + 1)
                            + " : " + best
                            + " | Fitness = "
                            + fitness(best, schedule)
            );
        }

        System.out.println("\nJadwal Akhir:");

        for (Individual item : schedule) {
            System.out.println(
                    item.kelas + " - "
                            + item.subject
                            + " oleh "
                            + item.teacher
                            + " pada "
                            + item.timeslot
            );
        }
    }
}