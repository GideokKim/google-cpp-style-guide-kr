# sizeof (sizeof)

## 원문 규칙 번역

sizeof( type ) 보다 sizeof( varname ) 을 선호합니다.

특정 변수의 크기를 구할 때는 sizeof( varname )을 사용하세요. sizeof( varname )은 누군가 지금 또는 나중에 변수 유형을 변경하면 적절하게 업데이트됩니다. 적절한 C++ 유형의 변수가 편리하지 않은 외부 또는 내부 데이터 형식을 관리하는 코드와 같이 특정 변수와 관련되지 않은 코드에 sizeof( type )을 사용할 수 있습니다.

```cpp
MyStruct data;
memset(&data, 0, sizeof(data));
```

```cpp
memset(&data, 0, sizeof(MyStruct));
```

```cpp
if (raw_size < sizeof(int)) {
  LOG(ERROR) << "compressed record not big enough for count: " << raw_size;
  return false;
}
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 적절한 C++ 유형의 변수가 편리하지 않은 외부 또는 내부 데이터 형식을 관리하는 코드와 같이 특정 변수와 관련되지 않은 코드에 sizeof( type )을 사용할 수 있습니다.

실제로 코드를 볼 때는 특정 변수의 크기를 구할 때는 sizeof( varname )을 사용하세요.

점검할 때는 특히 다음을 확인하세요:

- sizeof( varname )은 누군가 지금 또는 나중에 변수 유형을 변경하면 적절하게 업데이트됩니다.
- sizeof( varname ) 을 선호합니다.
