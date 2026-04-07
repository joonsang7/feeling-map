public class Student {
    private String id;
    private String name;
    private int java;
    private int db;
    private int security;
    private boolean hasGrades;

    public Student(String id, String name) {
        this.id = id;
        this.name = name;
        this.hasGrades = false;
    }

    public void registerGrades(int java, int db, int security) {
        this.java = java;
        this.db = db;
        this.security = security;
        this.hasGrades = true;
    }

    public boolean hasGrades() {
        return hasGrades;
    }

    public int getTotal() {
        return java + db + security;
    }

    public double getAverage() {
        return getTotal() / 3.0;
    }

    public String getGrade() {
        double avg = getAverage();
        if (avg >= 90) return "A";
        else if (avg >= 80) return "B";
        else return "C";
    }

    public String getId() { return id; }
    public String getName() { return name; }
}
