# 람다 표현식 형식 (Lambda Expressions)

다른 함수와 마찬가지로 매개변수와 본문의 형식을 지정하고 다른 쉼표로 구분된 목록과 같이 목록을 캡처합니다.

참조 기반 캡처의 경우 앰퍼샌드( & )와 변수 이름 사이에 공백을 두지 마십시오.

```cpp
int x = 0;
auto x_plus_n = [&x](int n) -> int { return x + n; }
```

짧은 람다는 함수 인수로 인라인으로 작성할 수 있습니다.

```cpp
absl::flat_hash_set<int> to_remove = {7, 8, 9};
std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
digits.erase(std::remove_if(digits.begin(), digits.end(), [&to_remove](int i) {
               return to_remove.contains(i);
             }),
             digits.end());
```

---

## 이해하기 쉽게 설명하기

### 핵심: 일반 함수처럼, 캡처 목록은 쉼표 목록처럼

람다의 매개변수·본문은 다른 함수와 똑같이 형식을 맞추고, 캡처 목록은 다른 쉼표 구분 목록처럼 씁니다.

```cpp
int x = 0;
auto x_plus_n = [&x](int n) -> int { return x + n; };  // &와 변수 이름 사이 공백 없음
```

### 짧은 람다는 인라인으로

짧은 람다는 함수 인수 자리에 인라인으로 써도 됩니다.

```cpp
digits.erase(std::remove_if(digits.begin(), digits.end(), [&to_remove](int i) {
               return to_remove.contains(i);
             }),
             digits.end());
```
