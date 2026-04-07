import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {

    /*
     * professor은 학생의 자바,db,보안 과목의 성적을 등록한다 (학생 id 체크)
     * 등록된 성적의 총합과 평균을 구한다.
     * 학생은 A,B,C 등급의 학점을 조회할 수 있다.(학생 id 체크)
     *
     * 프로그램이 시작되면, 1.학생 2.교수 3.종료 를 입력받고, 학생이면 학생 id를 입력받고, 교수면 교수 id를 입력받는다. (id 체크)
     *
     * 학생을 입력받으면 1. 신규 등록 2. 성적 조회를 입력받는다. 신규 등록이면 학생 id와 이름을 입력받아서 학생 객체를 생성한다.
     * 성적 조회면 학생 id를 입력받아서 성적이 존재하면 총합, 평균, 학점을 출력하고, 존재하지 않으면 "학생 정보가 없습니다."라고 출력한다.
     *
     * 교수를 입력받으면 1. 신규 등록 2. 성적 등록을 입력받는다. 신규 등록이면 교수 id와 이름을 입력받아서 교수 객체를 생성한다.
     * 성적 등록이면 학생 id와 자바, db, 보안 과목의 점수를 입력받아서 학생 id가 존재하면 성적을 등록하고,
     * 존재하지 않으면 "학생 정보가 없습니다."라고 출력한다.
     *
     * 등록하거나 조회할때는 id 체크를 한다. id가 존재하면 등록 또는 조회가 가능하고, 존재하지 않으면 등록 또는 조회가 불가능하다.
     */

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Map<String, Student> students = new HashMap<>();
        Map<String, Professor> professors = new HashMap<>();

        while (true) {
            System.out.println("\n1. 학생 2. 교수 3. 종료");
            int choice = scanner.nextInt();
            scanner.nextLine();

            if (choice == 3) {
                System.out.println("프로그램을 종료합니다.");
                break;

            } else if (choice == 1) {
                // 학생 메뉴
                System.out.println("1. 신규 등록 2. 성적 조회");
                int studentChoice = scanner.nextInt();
                scanner.nextLine();

                if (studentChoice == 1) {
                    // 신규 등록: id 중복 체크
                    System.out.print("학생 ID: ");
                    String id = scanner.nextLine();
                    if (students.containsKey(id)) {
                        System.out.println("이미 존재하는 학생 ID입니다.");
                        continue;
                    }
                    System.out.print("이름: ");
                    String name = scanner.nextLine();
                    students.put(id, new Student(id, name));
                    System.out.println(name + " 학생이 등록되었습니다.");

                } else if (studentChoice == 2) {
                    // 성적 조회: id 존재 체크
                    System.out.print("학생 ID: ");
                    String id = scanner.nextLine();
                    if (!students.containsKey(id)) {
                        System.out.println("학생 정보가 없습니다.");
                        continue;
                    }
                    Student student = students.get(id);
                    if (!student.hasGrades()) {
                        System.out.println("등록된 성적이 없습니다.");
                        continue;
                    }
                    System.out.println("이름: " + student.getName());
                    System.out.println("총합: " + student.getTotal());
                    System.out.printf("평균: %.2f%n", student.getAverage());
                    System.out.println("학점: " + student.getGrade());

                } else {
                    System.out.println("잘못된 입력입니다.");
                }

            } else if (choice == 2) {
                // 교수 메뉴
                System.out.println("1. 신규 등록 2. 성적 등록");
                int profChoice = scanner.nextInt();
                scanner.nextLine();

                if (profChoice == 1) {
                    // 신규 등록: id 중복 체크
                    System.out.print("교수 ID: ");
                    String id = scanner.nextLine();
                    if (professors.containsKey(id)) {
                        System.out.println("이미 존재하는 교수 ID입니다.");
                        continue;
                    }
                    System.out.print("이름: ");
                    String name = scanner.nextLine();
                    professors.put(id, new Professor(id, name));
                    System.out.println(name + " 교수님이 등록되었습니다.");

                } else if (profChoice == 2) {
                    // 성적 등록: 교수 id 체크 후 학생 id 체크
                    System.out.print("교수 ID: ");
                    String profId = scanner.nextLine();
                    if (!professors.containsKey(profId)) {
                        System.out.println("교수 정보가 없습니다.");
                        continue;
                    }

                    System.out.print("학생 ID: ");
                    String studentId = scanner.nextLine();
                    if (!students.containsKey(studentId)) {
                        System.out.println("학생 정보가 없습니다.");
                        continue;
                    }

                    System.out.print("자바 점수: ");
                    int java = scanner.nextInt();
                    System.out.print("DB 점수: ");
                    int db = scanner.nextInt();
                    System.out.print("보안 점수: ");
                    int security = scanner.nextInt();
                    scanner.nextLine();

                    students.get(studentId).registerGrades(java, db, security);
                    System.out.println("성적이 등록되었습니다.");

                } else {
                    System.out.println("잘못된 입력입니다.");
                }

            } else {
                System.out.println("잘못된 입력입니다.");
            }
        }

        scanner.close();
    }
}
