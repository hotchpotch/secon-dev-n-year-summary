from secon_d_summary.chain import build_chain

if __name__ == "__main__":
    url = "https://secon.dev/entry/2023/01/06/210000/"
    chain = build_chain()
    result = chain.invoke(url)
    print(result)
