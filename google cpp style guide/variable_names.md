# 변수 이름 (Variable Names)

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

## 이해하기 쉽게 설명하기

### 핵심: 변수는 snake_case, 클래스 멤버는 뒤에 밑줄

변수(함수 매개변수 포함)와 데이터 멤버는 `snake_case`(모두 소문자, 단어 사이 밑줄)로 씁니다.

```cpp
std::string table_name;  // OK
std::string tableName;   // 나쁨 - 혼합 대소문자
```

### 클래스 vs 구조체 멤버

- **클래스**의 데이터 멤버: 뒤에 밑줄 `_`을 붙입니다 → `table_name_`. (단, 정적 상수 멤버는 상수 명명 규칙 `kTableVersion`을 따름.)
- **구조체**의 데이터 멤버: 일반 변수처럼, 뒤에 밑줄 **없음** → `name`, `num_entries`.

```cpp
class TableInfo {
 public:
  static const int kTableVersion = 3;  // 상수 규칙
 private:
  std::string table_name_;             // 클래스 멤버 — 끝에 _
};

struct UrlTableProperties {
  std::string name;                    // 구조체 멤버 — _ 없음
  int num_entries;
};
```
