import pandas as pd
from features import (url_length, count_dots, has_ip_address, has_at_symbol,
                       count_hyphens, has_https, count_slashes, count_digits,
                       has_suspicious_words)


def build_features(input_file, output_file):
    df = pd.read_csv(input_file)

    # one column per feature function, applied across every url
    df["url_length"] = df["url"].apply(url_length)
    df["count_dots"] = df["url"].apply(count_dots)
    df["has_ip_address"] = df["url"].apply(has_ip_address)
    df["has_at_symbol"] = df["url"].apply(has_at_symbol)
    df["count_hyphens"] = df["url"].apply(count_hyphens)
    df["has_https"] = df["url"].apply(has_https)
    df["count_slashes"] = df["url"].apply(count_slashes)
    df["count_digits"] = df["url"].apply(count_digits)
    df["has_suspicious_words"] = df["url"].apply(has_suspicious_words)

    df.to_csv(output_file, index=False)
    return df


if __name__ == "__main__":
    df = build_features("phishing_sample.csv", "features_final.csv")
    print(df.shape)
    print(df.head())
