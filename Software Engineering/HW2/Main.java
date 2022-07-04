import java.util.*;

public class Main {
    public static Random rnd;

    public static void main(String[] args) {
        rnd = new Random(42);

        Folder fo1 = new Folder("B");
        File fi1 = new File("bye", "log");
        fo1.addItem(fi1);
        Folder fo2 = new Folder("A");
        fo2.addItem(fo1);
        File fi2 = new File("Aa", "txt");
        fi2.addContent("Hello\nWorld!");
        fo2.addItem(fi2);
        File fi3 = new File("aa", "py");
        fi3.addContent("print(\"Hello World\")");
        fo2.addItem(fi3);
        Folder fo3 = new Folder("C");
        File fi4 = new File("code", "java");
        fi4.addContent("class A {\n    public A() {\n        System.out.println(\"Hey there\");\n    }\n}");
        fo3.addItem(fi4);
        fo1.addItem(fo3);

        System.out.println("Sorting by size:");
        fo2.printTree(SortingField.SIZE);
        System.out.println("\n");

        System.out.println("Sorting by name:");
        fo2.printTree(SortingField.NAME);
        System.out.println("\n");

        System.out.println("Sorting by date:");
        fo2.printTree(SortingField.DATE);
        System.out.println("\n");

        String[] paths = {"aa.py", "B/code.java", "B/C/code.java", "AA.txt"};

        for (String path : paths) {
            File f = fo2.findFile(path);
            if (f == null) {
                System.out.println("File does not exist: " + path);
            } else {
                System.out.println("File has been found: " + path);
                f.printContent();
            }
            System.out.println("\n");
        }

        Folder f = new Folder("Testing");
        Folder temp1 = f;
        for (int i = 1; i <= 10; i++) {
            Folder temp2 = new Folder("temp" + i);
            temp1.addItem(temp2);
            temp1 = temp2;
        }
        temp1.addItem(new File("test2", "cs"));
        temp1.addItem(new File("test1", "cs"));

        f.printTree(SortingField.NAME);
    }
}
