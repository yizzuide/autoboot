# autoboot
一个Python语言的仿SpringBoot开发方式，支持IoC组件容器、注解式注册、配置驱动开发、事件通知、插件扩展的快速开发框架。
<p>
  <a href="https://pypi.org/project/autoboot">
      <img src="https://img.shields.io/pypi/v/autoboot?color=%2334D058&label=pypi%20package" alt="Version">
  </a>
  <a href="https://pypi.org/project/autoboot">
        <img src="https://img.shields.io/pypi/pyversions/autoboot.svg?color=%2334D058" alt="Python">
    </a>
    <a href="https://pepy.tech/project/autoboot">
        <img src="https://static.pepy.tech/personalized-badge/autoboot?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Downloads">
    </a>
    <a href="https://github.com/yizzuide/autoboot/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/yizzuide/autoboot" alt="License">
    </a>
</p>

## Purpose
在使用Python开发AI应用服务时遇到以下问题：

- 在`.env`里添加配置的方式，在获取配置参数时很容易写错，且调用没有代码提示。
- 配置参数较多时会让查找起来比较混乱，无法分类进行管理。
- 各种对象创建在各个函数和方法里，但多时候只需要创建一个单例。
- 很多代码和函数写在全局执行文件，创建的上下文数据在调用其它函数时需要层层传递。


## autoboot vs SpringBoot
由于Python有自身的语法特性，开发时也得到了天然的优化支持，以下是对比的测试环境：

| 开发语言 | 框架 | server |
| :----: | :----: | :----: |
| Python 3.11 | autoboot 0.7 | uvicorn
| Java 1.8 | SpringBoot 2.7 | Tomcat

- 不需要扫描组件所在的包，所有组件只需要声明即可（除Listener特殊组件需要配置扫描外）。
- 所有声明的组件只有在调用时才会创建并缓存，实现了SpringBoot推荐的懒加载创建方式。
- 配置采用`.env + yaml`组合，`.env`用于支持多环境配置项，主配置仅为`autoboot.yaml`，框架扩展了自定义指令`!env`用于从`.env`取值。
- 微服务项目的启动速度快到可以在1-2秒内启动完成，相比SpringBoot的10几秒，快了至少10倍。

## Quick Start

### Install
```bash
pip install autoboot
```

### Usage
#### 1. 导入并运行
```python
from autoboot import AutoBoot, AutoBootConfig

context = Autoboot(AutoBootConfig(config_dir="./config"))
context.run()
```

#### 2. 配置
* 启动配置文件：./config/.env

```ini
# 配置环境
ENV_NAME=dev

# 应用名
APPLICATION_NAME=demo
```

* 环境配置文件：./config/.env.dev

```ini
APPLICATION_NAME=demo-dev
```

* 主配置文件：./config/autoboot.yaml

```yml
autoboot:
  application:
    name: !env APPLICATION_NAME
    # 微服务模块名
    module: api
```

