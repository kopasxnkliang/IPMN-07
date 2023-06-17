# IPMN-07

## In Progress:
#### 1 Description words collection (100%)
#### 2 Data Preprocessing and set up our dataset (100%)
- online meeting with Prof. YIU at 10:30-11:100 on 6.23
#### 3 MVP-data-to-text Model Fine-tuning & Optimizing (In progress) - before 7.12
- fine-tune and select the model with lower training loss as well as higher generation score 
#### 4 API Implementation  (In progress) - before 7.12
- Frontend / Backend / API
#### 5 Final report - before 7.19


## System design details:
### 1. Backend -- Python
#### 1.1 Main approaches
Flask + json

Simple example in example folder.

#### 1.2 PDF Generation (Planning)
The original STR file is in Acrobat format, which is a 
closed source file format developed by Adobe. This means
it is nearly impossible to automatically edit the file.

### 2. Frontend -- Vue.js
    Framework: Vue3 (https://cn.vuejs.org/guide/quick-start.html)
    UI library: Element-plus (https://element-plus.org/zh-CN/)
    Http request: Axios (https://www.npmjs.com/package/vue-axios)

