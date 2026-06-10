# 클래스 형식 (Class Format)

## 원문 규칙 번역

public , protected 및 private 순서의 섹션은 각각 한 칸씩 들여쓰기됩니다.

클래스 정의의 기본 형식은 다음과 같습니다(주석이 없습니다. 어떤 주석이 필요한지에 대한 논의는 클래스 주석을 참조하세요).

```cpp
class MyClass : public OtherClass {
 public:      // Note the 1 space indent!
  MyClass();  // Regular 2 space indent.
  explicit MyClass(int var);
  MyClass(const MyClass& other);
  MyClass& operator=(const MyClass& other);
  ~MyClass() {}

  void SomeFunction();
  void SomeFunctionThatDoesNothing() {}

  void set_some_var(int var) { some_var_ = var; }
  int some_var() const { return some_var_; }

 private:
  bool SomeInternalFunction();

  int some_var_;
  int some_other_var_;
};
```

참고 사항:

- 모든 기본 클래스 이름은 하위 클래스 이름과 같은 줄에 있어야 하며 80열 제한이 적용됩니다.
- public: , protected: 및 private: 키워드는 한 칸 들여쓰기되어야 합니다.
- 첫 번째 인스턴스를 제외하고 이러한 키워드 앞에는 빈 줄이 와야 합니다. 이 규칙은 소규모 클래스에서는 선택 사항입니다.
- 이러한 키워드 뒤에 빈 줄을 두지 마십시오.
- 공개 섹션이 먼저 오고, 보호 섹션이 그 뒤를 따르고, 마지막으로 비공개 섹션이 와야 합니다.
- 각 섹션 내에서 선언 순서 지정에 대한 규칙은 선언 순서를 참조하세요.

---

## 이해하기 쉽게 설명하기

클래스 형식 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
