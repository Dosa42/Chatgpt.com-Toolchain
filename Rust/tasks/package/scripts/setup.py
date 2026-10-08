"""Set up the source, target tools and Rust toolchain for this task."""
def setup(context):
    from shared.run import setup as shared_setup
    shared_setup(context)
