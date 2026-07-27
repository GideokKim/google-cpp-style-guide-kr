# 접근 제어 (Access Control)

클래스의 데이터 멤버가 상수가 아닌 한 비공개로 만듭니다. 이는 필요한 경우 접근자(보통 const ) 형태의 쉬운 상용구를 사용하여 불변성에 대한 추론을 단순화합니다.

기술적인 이유로 Google Test를 사용할 때 .cc 파일에 정의된 테스트 픽스처 클래스의 데이터 멤버를 보호할 수 있습니다. 테스트 픽스처 클래스가 .cc 파일 외부에서 정의된 경우(예: .h 파일) 데이터 멤버를 비공개로 만듭니다.

---

## 옮긴이 풀이

### 핵심: 데이터 멤버는 private (상수 제외)

클래스의 데이터 멤버는 상수가 아닌 한 `private`으로 두세요. 그러면 그 값을 누가 언제 바꾸는지가 클래스 안으로 한정되어, 불변식을 추론하기 쉬워집니다. 외부에서 읽거나 써야 하면 접근자(getter, 보통 `const`)·설정자(setter)를 두세요.

```cpp
class Widget {
 public:
  int width() const { return width_; }   // 접근자
  void set_width(int w) { width_ = w; }   // 설정자
 private:
  int width_;                             // 데이터는 private
};
```

### 예외

Google Test의 테스트 픽스처 클래스가 `.cc` 파일 안에 정의된 경우, 기술적 이유로 데이터 멤버를 `protected`로 둘 수 있습니다. 픽스처가 `.h` 파일 등 외부에 정의되면 다시 `private`으로 하세요.
