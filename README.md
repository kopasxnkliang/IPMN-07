# IPMN-07

## In Progress:
### 1. Description words / figures collection (90%)
### 2. Data Preprocessing (filtering) and set up our dataset (using OpenNRE) (10%)
### 3. MVP-data-to-text Model Fine-tuning / GPT Fine-tuning
### 4. API Implementation

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
