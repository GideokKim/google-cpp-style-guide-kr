# 매크로 이름 (Macro Names)

## 원문 규칙 번역

당신은 실제로 매크로를 정의하지 않을 것입니다. 그렇죠? 그렇게 하면 MY_MACRO_THAT_SCARES_SMALL_CHILDREN_AND_ADULTS_ALIKE 와 같습니다.

매크로 설명을 참조하세요. 일반적으로 매크로는 사용하면 안 됩니다. 그러나 꼭 필요한 경우에는 모두 대문자와 밑줄, 프로젝트별 접두사를 사용하여 이름을 지정해야 합니다.

```cpp
#define MYPROJECT_ROUND(x) ...
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 그러나 꼭 필요한 경우에는 모두 대문자와 밑줄, 프로젝트별 접두사를 사용하여 이름을 지정해야 합니다.

실제로 코드를 볼 때는 당신은 실제로 매크로를 정의하지 않을 것입니다.

점검할 때는 특히 다음을 확인하세요:

- 그렇게 하면 MY_MACRO_THAT_SCARES_SMALL_CHILDREN_AND_ADULTS_ALIKE 와 같습니다.
