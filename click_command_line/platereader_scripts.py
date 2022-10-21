import click


@click.command()
@click.option("--data_file", required=True,
              help="Data file for analysis. Different conditions must be different groups in the plate layout")
@click.option('--labels', required=True, help='Labels for the figure legend separated by commas (no spaces)')
@click.option('--fluorophores', required=True,
              help='The fluorophores used in the experiment in the order set separated by commas (no spaces)')
def click_multiplex_cleanup(**kwargs):
    from platereader.multiplexing import cleanup_multiplex_data

    cleanup_multiplex_data(**kwargs)


@click.command()
@click.option('--data_file', required=True,
              help='Data file for analysis. Different conditions must be different groups in the plate layout.')
@click.option('--labels', required=True, help='Labels for the figure legend separated by commas (no spaces)')
def click_interpret_kinetics(**kwargs):
    from platereader.kinetics import interpret_plate_kinetics

    interpret_plate_kinetics(**kwargs)
