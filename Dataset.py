class Dataset:
    def __init__(self, pd_dataframe_read):
        self.df = pd_dataframe_read
        # each operation should be marked as active through a decorator
        # (regaz secondo me si può mettere "status" come parametro e il decorator cambia il parametro con "active o "inactive"")
        # ma non saprei come fare quindi I only did it for the Vine
    #def get_df(self):


  #fai un getter