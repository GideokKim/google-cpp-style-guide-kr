# 함수 호출 (Function Calls)

호출을 모두 한 줄에 작성하거나, 인수를 괄호로 묶거나, 4개의 공백으로 들여쓰기된 새 줄에서 인수를 시작하고 4개의 공백 들여쓰기에서 계속합니다. 다른 고려 사항이 없으면 적절한 경우 각 줄에 여러 인수를 배치하는 것을 포함하여 최소 줄 수를 사용하십시오.

함수 호출의 형식은 다음과 같습니다.

```cpp
bool result = DoSomething(argument1, argument2, argument3);
```

인수가 한 줄에 모두 들어가지 않으면 여러 줄로 나누어야 하며, 이후의 각 줄은 첫 번째 인수에 맞춰 정렬되어야 합니다. 열린 괄호 뒤나 닫는 괄호 앞에 공백을 추가하지 마세요.

```cpp
bool result = DoSomething(averyveryveryverylongargument1,
                          argument2, argument3);
```

선택적으로 인수는 4개의 공백 들여쓰기를 사용하여 다음 줄에 모두 배치될 수 있습니다.

```cpp
if (...) {
  ...
  ...
  if (...) {
    bool result = DoSomething(
        argument1, argument2,  // 4 space indent
        argument3, argument4);
    ...
  }
```

특정 가독성 문제가 없는 한 함수 호출에 필요한 줄 수를 줄이려면 한 줄에 여러 인수를 입력하세요. 어떤 사람들은 각 줄에 하나의 인수만 사용하여 형식을 지정하는 것이 더 읽기 쉽고 인수 편집을 단순화한다는 사실을 발견했습니다. 그러나 우리는 인수 편집의 용이성보다 독자를 우선시하며 대부분의 가독성 문제는 다음 기술을 통해 더 잘 해결됩니다.

한 줄에 여러 개의 인수가 있으면 일부 인수를 구성하는 표현식의 복잡성이나 혼란으로 인해 가독성이 떨어지는 경우 해당 인수를 설명적인 이름으로 캡처하는 변수를 만들어 보십시오.

```cpp
int my_heuristic = scores[x] * y + bases[x];
bool result = DoSomething(my_heuristic, x, y, z);
```

또는 설명 주석과 함께 혼란스러운 주장을 한 줄에 넣으십시오.

```cpp
bool result = DoSomething(scores[x] * y + bases[x],  // Score heuristic.
                          x, y, z);
```

한 인수가 한 줄에 훨씬 더 읽기 쉬운 경우가 여전히 있다면, 별도의 줄에 넣으십시오. 결정은 일반적인 정책보다는 더 읽기 쉬운 주장에 구체적이어야 합니다.

때때로 인수는 가독성에 중요한 구조를 형성합니다. 이러한 경우에는 해당 구조에 따라 인수 형식을 자유롭게 지정하세요.

```cpp
// Transform the widget by a 3x3 matrix.
my_widget.Transform(x1, x2, x3,
                    y1, y2, y3,
                    z1, z2, z3);
```

---

## 이해하기 쉽게 설명하기

### 핵심: 한 줄에, 안 되면 4칸 들여써서 래핑

함수 호출은 한 줄에 쓰거나, 인수가 넘치면 줄을 나눠 첫 인수에 맞춰 정렬하거나, 4칸 들여쓰기로 다음 줄에 모읍니다. 특별한 이유가 없으면 **줄 수를 최소화**하세요(한 줄에 여러 인수 포함).

```cpp
bool result = DoSomething(argument1, argument2, argument3);

bool result = DoSomething(averyveryveryverylongargument1,
                          argument2, argument3);

bool result = DoSomething(
    argument1, argument2,  // 4칸 들여쓰기
    argument3, argument4);
```

### 인수가 복잡해 읽기 어려우면

"한 줄 한 인수"보다, 복잡한 인수를 **명명된 변수**로 빼거나 **설명 주석**을 다는 편이 낫습니다.

```cpp
int my_heuristic = scores[x] * y + bases[x];
bool result = DoSomething(my_heuristic, x, y, z);
```

### 인수가 구조를 이루면

인수가 가독성에 중요한 구조(예: 3×3 행렬)를 이루면, 그 구조에 맞춰 자유롭게 배치하세요.
