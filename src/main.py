import os

from fastText import *
from sklearn.metrics import confusion_matrix

def print_results(N, p, r, model_params):
    os.makedirs("results/", exist_ok=True)

    with open("results/result.txt", "w") as f:
        f.write("---------- Parameters --------------\n")
        f.write("Epoch: {0}\n".format(model_params["epoch"]))
        f.write("Learning rate: {0}\n".format(model_params["learning_rate"]))
        f.write("N-Grams: {0}\n".format(model_params["n_grams"]))
        f.write("Min Count: {0}\n".format(model_params["min_count"]))
        f.write("Loss: {0}\n".format(model_params["loss"]))

        f.write("\n---------- Results -----------------\n")
        f.write("N\t" + str(N))
        f.write('\n')
        f.write("P@{}\t{:.3f}".format(1, p))
        f.write('\n')
        f.write("R@{}\t{:.3f}".format(1, r))
        f.write('\n')

        print("---------- Parameters --------------\n")
        print("Epoch: {0}\n".format(model_params["epoch"]))
        print("Learning rate: {0}\n".format(model_params["learning_rate"]))
        print("N-Grams: {0}\n".format(model_params["n_grams"]))
        print("Min Count: {0}\n".format(model_params["min_count"]))
        print("Loss: {0}\n".format(model_params["loss"]))

        print("\n---------- Results -----------------\n")
        print("N\t" + str(N))
        print('\n')
        print("P@{}\t{:.3f}".format(1, p))
        print('\n')
        print("R@{}\t{:.3f}".format(1, r))
        print('\n')


def train():
    data = 'data/'
    train_data = os.path.join(data, 'news.train')

    # max_model = {}
    # max_p = 0
    # setting = {}
    # for lr in frange(0.1,1,0.1):
    #     for epoch in range(10,100,10):
    #         for wordNgrams in range(1,5,1):
    #             model = train_supervised(
    #                 input=train_data, epoch=epoch,lr=lr, wordNgrams=2, minCount=1,
    #                 loss="hs"
    #             )
    #             M,p,q = model.test(valid_data)
    #             if(p > max_p):
    #                 max_model = model
    #                 max_p = p
    #                 settings = [lr,epoch,wordNgrams]
    #                 print(settings)
    #
    #             print(p)
    # print("Best settings")
    # print(settings)
    # print(p)

    epoch = 100
    learning_rate = 0.1
    n_grams = 2
    min_count = 1
    loss = "hs"

    model_params = {
        "epoch": epoch,
        "learning_rate": learning_rate,
        "n_grams": n_grams,
        "min_count": min_count,
        "loss": loss
    }

    model = train_supervised(
        input=train_data, epoch=epoch, lr=learning_rate, wordNgrams=n_grams, minCount=min_count,
        loss=loss
    )

    model.save_model("model.bin")

    # print("\n");
    # print("\n------- Quantized Start -------------\n")
    # model.quantize(input=train_data, qnorm=True, retrain=True, cutoff=100000)
    # model.save_model("model.ftz")
    # print("\n------- Quantized Stop --------------\n")


if __name__ == "__main__":
    data = 'data/'
    # train()

    model = load_model("model.bin")

    valid_data = open(os.path.join(data, 'news.valid'), "r", encoding="utf8").read()
    valid_labels = []
    valid_articles = []

    for v in valid_data.split("\n"):
        split = v.find(" ")
        valid_labels.append(v[0:split])
        valid_articles.append(v[split:])

    pred_labels = []
    for a in valid_articles:
        pred_label = model.predict(a)
        pred_labels.append(pred_label[0][0])

    print(confusion_matrix(valid_labels, pred_labels, labels=["__label__diepresse", "__label__krone", "__label__derstandard"]))

    epoch = 100
    learning_rate = 0.1
    n_grams = 2
    min_count = 1
    loss = "hs"

    model_params = {
        "epoch": epoch,
        "learning_rate": learning_rate,
        "n_grams": n_grams,
        "min_count": min_count,
        "loss": loss
    }

    print_results(*model.test("data/news.valid"), model_params)
