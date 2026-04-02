#!/usr/bin/env python3
import urllib.request
import yaml
import sys
import os

# 这是一个自动为您生成包含美国节点的完整配置文件的脚本
# 它可以完美避开 Clash Verge 的任何合并 Bug

SUBSCRIPTION_URL = "https://app.mitce.net/api/v1/client/subscribe?token=your_token_here" # 请在执行前替换为您真实的订阅链接
OUTPUT_FILE = "clash_claude_chain.yaml"

def build_profile():
    print("正在下载原始订阅...")
    try:
        # 考虑到某些订阅链接可能需要伪装 User-Agent
        req = urllib.request.Request(SUBSCRIPTION_URL, headers={'User-Agent': 'ClashMeta'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"下载订阅失败，请确保 URL 正确: {e}")
        # 如果下载失败，我们尝试读取本地可能存在的订阅文件，这里为了演示，只处理网络下载
        return

    print("正在解析配置...")
    try:
        config = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"解析 YAML 失败: {e}")
        return

    print("正在注入美国 Socks5 节点和代理链...")
    # 1. 注入节点
    us_node = {
        'name': 'US-Claude-Socks5',
        'type': 'socks5',
        'server': '77.111.118.251',
        'port': 42136,
        'username': '1EDHhzBv3DDgLSe',
        'password': 'dwi3ANd0cvCUBWv',
        'udp': True
    }
    
    if 'proxies' not in config:
        config['proxies'] = []
    config['proxies'].append(us_node)

    # 2. 注入代理链策略组 (使用最稳定的 relay)
    chain_group = {
        'name': 'Claude-Chain',
        'type': 'relay',
        'proxies': ['JP-2', 'US-Claude-Socks5'] # 假设您的列表里有 JP-2，如果没有，后续可以手动改
    }
    
    if 'proxy-groups' not in config:
        config['proxy-groups'] = []
    config['proxy-groups'].insert(0, chain_group) # 放到最前面方便找

    # 3. 将新节点和链加入全局选择器 (如果存在)
    for group in config.get('proxy-groups', []):
        if group['name'] == 'PROXIES' or group['name'] == 'Proxy':
            if 'proxies' in group:
                group['proxies'].insert(0, 'Claude-Chain')
                group['proxies'].append('US-Claude-Socks5')

    # 4. 注入规则
    rules_to_inject = [
        'DOMAIN-SUFFIX,claude.ai,Claude-Chain',
        'DOMAIN-SUFFIX,anthropic.com,Claude-Chain',
        'DOMAIN-SUFFIX,chatgpt.com,Claude-Chain',
        'DOMAIN-SUFFIX,openai.com,Claude-Chain'
    ]
    
    if 'rules' not in config:
        config['rules'] = []
    
    # 将规则插在最前面以确保最高优先级
    config['rules'] = rules_to_inject + config['rules']

    print(f"正在保存最终配置到 {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)
    
    print("配置生成成功！")

if __name__ == "__main__":
    build_profile()