# 변수 이름 (Variable Names)

## 원문 규칙 번역

변수(함수 매개변수 포함) 및 데이터 멤버의 이름은 snake_case(모두 소문자, 단어 사이에 밑줄 포함)입니다. 클래스(구조체 제외)의 데이터 멤버에는 추가로 후행 밑줄이 있습니다. 예를 들면: a_local_variable , a_struct_data_member , a_class_data_member_ .

예를 들어:

```cpp
std::string table_name;  // OK - snake_case.
```

```cpp
std::string tableName;   // Bad - mixed case.
```

정적 및 비정적 클래스의 데이터 멤버는 일반 비멤버 변수처럼 이름이 지정되지만 뒤에 밑줄이 붙습니다. 이에 대한 예외는 상수 명명 규칙을 따라야 하는 정적 상수 클래스 멤버입니다.

```cpp
class TableInfo {
 public:
  ...
  static const int kTableVersion = 3;  // OK - constant naming.
  ...

 private:
  std::string table_name_;             // OK - underscore at end.
  static Pool<TableInfo>* absl_nullable pool_;       // OK.
};
```

정적 및 비정적 구조체의 데이터 멤버는 일반 비멤버 변수처럼 이름이 지정됩니다. 클래스의 데이터 멤버에 있는 후행 밑줄이 없습니다.

```cpp
struct UrlTableProperties {
  std::string name;
  int num_entries;
  static Pool<UrlTableProperties>* absl_nullable pool;
};
```

구조체와 클래스를 언제 사용해야 하는지에 대한 논의는 구조체와 클래스를 참조하세요.

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 구조체와 클래스를 언제 사용해야 하는지에 대한 논의는 구조체와 클래스를 참조하세요.

실제로 코드를 볼 때는 예를 들면: a_local_variable , a_struct_data_member , a_class_data_member_ .

점검할 때는 특히 다음을 확인하세요:

- 변수(함수 매개변수 포함) 및 데이터 멤버의 이름은 snake_case(모두 소문자, 단어 사이에 밑줄 포함)입니다.
- 예를 들어: 정적 및 비정적 클래스의 데이터 멤버는 일반 비멤버 변수처럼 이름이 지정되지만 뒤에 밑줄이 붙습니다.
