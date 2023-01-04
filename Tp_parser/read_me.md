# # Rule File Generation

## Supported templates
* iCCmemDecodeTest
* iCAnalogMeasureTest
* iCDCLeakageTest

## Required arguments
1. Modules path
2. Module Name
3. Output path

## Steps to run
```python

if __name__ == "__main__":
    modulePath = "I:/hdmxprogs/wlw/WLWXXXXA0H10A60S053/Modules"
    mp = MtplParser(modulePath,'SIO_SERDES')
    mp.rule_file_gen(output_path="C:/temp/rule_file")
  
```

## Output files

![image](https://user-images.githubusercontent.com/102200730/210474369-f10c894d-cc72-47e6-9468-4c4f0d92a38d.png)
