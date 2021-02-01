import os

class Arguments:
    """
    Let the user enter the argument via command line.
    """

    def __init__(self, argv, prefix=""):
        if len(argv) != 6:
            usage(argv)

        # initializing default values
        self.instance = argv[1]
        self.num_nodes = int(argv[2])
        self.num_flows = int(argv[3])
        self.num_items = int(argv[4])
        self.num_mon_app = int(argv[5])
        self.min_size = 1
        self.max_size = 5
        self.edges_to_attach = 2


def usage(argv):
    """
    Prints the usage of the software, including all possible arguments.
    :param argv: arguments passed by the user.
    """
    exe = os.path.basename(argv[0])
    print("")
    print("Usage: " + exe + " <instance_file> " + " <|D|> " + " <|F|> " + " <|V|> " + " <|M|> ")
    print("")
    print("Example: " + exe + " data/instances " + " 50 " + " 100 " + " 8 " + " 4 ")
    print("")
    exit(1)
