// Define the main function (Do not change the function name)
function main(config) {
  // 1. 注入您的美国 Socks5 节点
  const mySocks5 = {
    name: "US-Claude-Socks5",
    type: "socks5",
    server: "77.111.118.251",
    port: 42136,
    username: "1EDHhzBv3DDgLSe",
    password: "dwi3ANd0cvCUBWv", // 已经为您填好真实密码
    udp: true
  };
  
  if (!config.proxies) config.proxies = [];
  config.proxies.push(mySocks5);

  // 2. 创建代理链 (Relay) 策略组
  const myRelayGroup = {
    name: "Claude-Chain",
    type: "relay",
    // 确保 "JP-2" 是您订阅列表里真实存在的节点名
    proxies: ["JP-2", "US-Claude-Socks5"]
  };

  if (!config["proxy-groups"]) config["proxy-groups"] = [];
  
  // 将代理链策略组插入到最前面
  config["proxy-groups"].unshift(myRelayGroup);

  // 3. 将代理链加入到主选择器 (PROXIES 或 节点选择) 中，方便您手动切换
  // 假设您的主选择器叫 "PROXIES" 或 "节点选择"，我们这里做个通用的追加
  for (let group of config["proxy-groups"]) {
    if (group.type === "select" && group.proxies) {
      if (!group.proxies.includes("Claude-Chain")) {
         group.proxies.push("Claude-Chain");
      }
    }
  }

  // 4. 强制让 Claude 走代理链
  if (!config.rules) config.rules = [];
  const myRules = [
    "DOMAIN-SUFFIX,claude.ai,Claude-Chain",
    "DOMAIN-SUFFIX,anthropic.com,Claude-Chain",
    "DOMAIN-SUFFIX,chatgpt.com,Claude-Chain",
    "DOMAIN-SUFFIX,openai.com,Claude-Chain"
  ];
  
  // 把规则插到最前面
  config.rules = myRules.concat(config.rules);

  return config;
}