import java.util.Random;

public class SmallTest {
    private static final Random rnd = new Random();
    private static final int NUM_ANIMALS = 100;
    private static final int NUM_ACTIONS = 30;
    private static ZooObserver[] observers = null;

    public static void setSeed(long seed) {
        rnd.setSeed(seed);
    }

    private static void initializeObservers() {
        String[] names = {"Avi", "Dani", "David", "Shahar", "Shimon", "Amit"};
        observers = new ZooObserver[names.length];
        for (int i = 0; i < names.length; i++) {
            observers[i] = new ZooObserver(names[i]);
        }
    }

    public static void runTest() {
        initializeObservers();

        Zoo zoo = Zoo.getInstance();
        Zoo zoo2 = Zoo.getInstance();

        System.out.println();
        AnimalFactory unicornFactory = new UnicornFactory();
        AnimalFactory zebraFactory = new ZebraFactory();
        AnimalFactory monkeyFactory = new MonkeyFactory();

        // Add the first half of observers
        for (int i = 0; i < observers.length / 2; i++) {
            zoo.addObserver(observers[i]);
        }


        // Add animals to zoo
        for (int i = 0; i < NUM_ANIMALS; i++) {
            switch (rnd.nextInt(3)) {
                case 0:
                    zoo.addAnimal(unicornFactory.createAnimal());
                    break;
                case 1:
                    zoo.addAnimal(zebraFactory.createAnimal());
                    break;
                case 2:
                    zoo.addAnimal(monkeyFactory.createAnimal());
                    break;
                default:
                    break;
            }
        }
        zoo.showAnimalsInfo();
        System.out.println();

        // Add the second half of observers
        for (int i = observers.length / 2; i< observers.length; i++) {
            zoo.addObserver(observers[i]);
        }

        System.out.println();

        // Generate actions
        for (int i = 0; i < NUM_ACTIONS; i++) {
            switch (rnd.nextInt(2)) {
                case 0:
                    zoo.feedAnimals();
                    break;
                case 1:
                    zoo.watchAnimals();
                    break;
                default:
                    break;
            }
            if (i == NUM_ACTIONS / 2) {
                zoo.removeObserver(observers[0]);
                zoo.removeObserver(observers[observers.length - 1]);
            }
            if (i % 10 == 0) {
                System.out.println();
                zoo.addAnimal(unicornFactory.createAnimal());
                zoo.showAnimalsInfo();
            }
            System.out.println();
        }
        zoo.showAnimalsInfo();
    }
}
